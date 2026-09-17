from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from customers.models import Customer
from menu.models import MenuCategory, MenuItem

from .models import Order, OrderItem

CART_SESSION_KEY = "online_cart"


def _get_cart(request):
    return request.session.get(CART_SESSION_KEY, {})


def _save_cart(request, cart):
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def _cart_items(request):
    """Resolves the session cart {item_id: qty} into real MenuItem rows + line totals."""
    cart = _get_cart(request)
    if not cart:
        return [], Decimal("0")

    items = MenuItem.objects.filter(pk__in=cart.keys(), is_available=True)
    lines = []
    subtotal = Decimal("0")
    for item in items:
        qty = int(cart.get(str(item.pk), 0))
        if qty < 1:
            continue
        line_total = item.price * qty
        subtotal += line_total
        lines.append({"item": item, "quantity": qty, "line_total": line_total})
    return lines, subtotal


def order_now(request):
    """
    The public 'Order Now' page -- a Foodpanda-style menu browser where a
    customer picks dishes and quantities, adds them to a cart, then checks
    out with a delivery address instead of being sent off-site.
    """
    categories = MenuCategory.objects.filter(is_active=True)
    items = MenuItem.objects.filter(is_available=True).select_related("category")
    cart = _get_cart(request)
    cart_count = sum(int(q) for q in cart.values()) if cart else 0

    context = {
        "categories": categories,
        "items": items,
        "cart_count": cart_count,
    }
    return render(request, "site/order_now.html", context)


def cart_add(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id, is_available=True)
    if request.method == "POST":
        try:
            quantity = max(1, int(request.POST.get("quantity", 1)))
        except (TypeError, ValueError):
            quantity = 1

        cart = _get_cart(request)
        key = str(item.pk)
        cart[key] = int(cart.get(key, 0)) + quantity
        _save_cart(request, cart)
        messages.success(request, f"Added {item.name} to your order.")

    return redirect(request.POST.get("next") or "order_now")


def cart_update(request, item_id):
    if request.method == "POST":
        cart = _get_cart(request)
        key = str(item_id)
        try:
            quantity = int(request.POST.get("quantity", 1))
        except (TypeError, ValueError):
            quantity = 1

        if quantity <= 0:
            cart.pop(key, None)
        else:
            cart[key] = quantity
        _save_cart(request, cart)
    return redirect("cart_view")


def cart_remove(request, item_id):
    if request.method == "POST":
        cart = _get_cart(request)
        cart.pop(str(item_id), None)
        _save_cart(request, cart)
    return redirect("cart_view")


def cart_view(request):
    lines, subtotal = _cart_items(request)

    if request.method == "POST" and "place_order" in request.POST:
        if not lines:
            messages.error(request, "Your cart is empty.")
            return redirect("order_now")

        name = request.POST.get("customer_name", "").strip()
        phone = request.POST.get("customer_phone", "").strip()
        address = request.POST.get("delivery_address", "").strip()
        notes = request.POST.get("special_instructions", "").strip()

        if not (name and phone and address):
            messages.error(request, "Please fill in your name, phone number, and delivery address.")
        else:
            customer = None
            if phone:
                customer, _created = Customer.objects.get_or_create(
                    phone=phone, defaults={"name": name}
                )

            order = Order.objects.create(
                order_type=Order.TYPE_ONLINE,
                customer=customer,
                customer_name=name,
                customer_phone=phone,
                delivery_address=address,
                special_instructions=notes,
            )
            for line in lines:
                OrderItem.objects.create(
                    order=order,
                    menu_item=line["item"],
                    quantity=line["quantity"],
                    unit_price=line["item"].price,
                )
            order.recalculate_totals()

            _save_cart(request, {})
            messages.success(request, f"Order placed! Your order number is {order.order_number}.")
            return redirect("order_confirmation", order_number=order.order_number)

    context = {
        "lines": lines,
        "subtotal": subtotal,
    }
    return render(request, "site/cart.html", context)


def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, order_type=Order.TYPE_ONLINE)
    return render(request, "site/order_confirmation.html", {"order": order})
