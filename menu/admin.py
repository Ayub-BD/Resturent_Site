from django.contrib import admin

from .models import MenuCategory, MenuItem, Offer


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "old_price", "is_available", "is_featured")
    list_editable = ("is_available", "is_featured")
    list_filter = ("category", "is_available", "is_featured")
    search_fields = ("name", "description")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "discount_percent", "start_date", "end_date", "is_active", "is_currently_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")

    @admin.display(boolean=True, description="Live now?")
    def is_currently_active(self, obj):
        return obj.is_currently_active
