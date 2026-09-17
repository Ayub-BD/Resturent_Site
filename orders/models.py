from django.db import models, transaction
from django.utils import timezone
from decimal import Decimal


class Order(models.Model):
    """
    One in-restaurant order created via the POS. Covers the full lifecycle
    from creation through kitchen prep to being served, per the spec's
    status flow: pending -> confirmed -> preparing -> ready -> served -> completed
    (with 'cancelled' as an off-ramp at any point before completion).
    """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_PREPARING = "preparing"
    STATUS_READY = "ready"
    STATUS_SERVED = "served"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_PREPARING, "Preparing"),
        (STATUS_READY, "Ready"),
        (STATUS_SERVED, "Served"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    PAYMENT_CASH = "cash"
    PAYMENT_CARD = "card"
    PAYMENT_MOBILE = "mobile_banking"

    PAYMENT_CHOICES = [
        (PAYMENT_CASH, "Cash"),
        (PAYMENT_CARD, "Card"),
        (PAYMENT_MOBILE, "Mobile Banking"),
    ]

    TYPE_DINE_IN = "dine_in"
    TYPE_ONLINE = "online"

    TYPE_CHOICES = [
        (TYPE_DINE_IN, "Dine-in"),
        (TYPE_ONLINE, "Online / Delivery"),
    ]

    order_number = models.CharField(max_length=20, unique=True, editable=False)

    order_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default=TYPE_DINE_IN,
        help_text="Dine-in orders are created from the POS with a table. Online orders "
                   "come from the website's 'Order Now' page and are delivered instead.",
    )

    table = models.ForeignKey(
        "tables.RestaurantTable", on_delete=models.SET_NULL, related_name="orders",
        blank=True, null=True,
        help_text="Required for dine-in orders. Left blank for online/delivery orders.",
    )

    # Only used for online/delivery orders, where there is no Staff-managed
    # Customer record yet -- the customer types these in at checkout.
    customer_name = models.CharField(max_length=100, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    delivery_address = models.TextField(blank=True)

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders",
    )
    created_by = models.ForeignKey(
        "accounts.Staff",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders_created",
        help_text="The waiter/manager who created this order.",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, blank=True
    )
    special_instructions = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_number} - {self.table or 'Delivery'}"

    @property
    def is_online(self):
        return self.order_type == self.TYPE_ONLINE

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_order_number():
        """
        Generates ORD-0001, ORD-0002, ... using a DB transaction + row lock
        so two waiters confirming orders at the same moment can never get
        the same number (the spec explicitly requires no duplicates).
        """
        with transaction.atomic():
            last_order = (
                Order.objects.select_for_update()
                .order_by("-id")
                .first()
            )
            next_id = (last_order.id + 1) if last_order else 1
            return f"ORD-{next_id:04d}"

    def recalculate_totals(self):
        """Recompute subtotal/total from line items. Call after adding/removing items."""
        items_total = sum((item.line_total for item in self.items.all()), Decimal('0.00'))
        self.subtotal = items_total
        
        # এখানে current_discount ভেরিয়েবলটি ডিক্লেয়ার করা হয়েছিল কিন্তু নিচে ব্যবহার করা হয়নি
        current_discount = Decimal(str(self.discount or '0.00'))
        
        # self.discount এর বদলে এখন current_discount ব্যবহার করা হলো
        self.total = max(items_total - current_discount, Decimal('0.00'))
        self.save(update_fields=["subtotal", "total"])

    def set_status(self, new_status, changed_by=None):
        """
        The single place status changes happen, so every transition is
        automatically logged to OrderStatusHistory -- no view should ever
        set `order.status = ...` directly.
        """
        self.status = new_status
        self.save(update_fields=["status", "updated_at"])
        OrderStatusHistory.objects.create(
            order=self, status=new_status, changed_by=changed_by
        )


class OrderItem(models.Model):
    """
    One line item within an order. unit_price is a SNAPSHOT of the menu
    item's price at order time -- deliberately duplicated so that if the
    manager changes menu prices later, past receipts stay accurate.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(
        "menu.MenuItem", on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.CharField(
        max_length=200, blank=True, help_text="e.g. 'No onion' -- shown on the kitchen ticket."
    )

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.menu_item.price
        super().save(*args, **kwargs)

    @property
    def line_total(self):
        return self.unit_price * self.quantity


class OrderStatusHistory(models.Model):
    """
    An audit trail entry: who changed an order to which status, and when.
    Powers the dashboard's live order tracking without any extra bookkeeping
    -- just read this table instead of guessing from timestamps.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    changed_by = models.ForeignKey(
        "accounts.Staff", on_delete=models.SET_NULL, blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
        verbose_name_plural = "Order status history"

    def __str__(self):
        return f"{self.order.order_number} -> {self.status} @ {self.timestamp:%H:%M}"


class Payment(models.Model):
    """
    Records the actual payment for a completed order. Kept separate from
    Order (rather than just using Order.payment_method) so refunds/partial
    payments have somewhere to live later without restructuring Order.
    """

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=20, choices=Order.PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.order.order_number} - {self.amount} via {self.get_method_display()}"
