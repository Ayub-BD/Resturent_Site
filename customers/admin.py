from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "order_count", "total_spent")
    search_fields = ("name", "phone", "email")

    @admin.display(description="Orders")
    def order_count(self, obj):
        return obj.order_count

    @admin.display(description="Total Spent")
    def total_spent(self, obj):
        return obj.total_spent
