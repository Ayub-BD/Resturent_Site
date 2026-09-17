from django.shortcuts import render

from .models import MenuCategory, MenuItem


def menu_list(request):
    categories = MenuCategory.objects.filter(is_active=True)
    items = MenuItem.objects.filter(is_available=True).select_related("category")

    context = {
        "categories": categories,
        "items": items,
    }
    return render(request, "site/menu.html", context)
