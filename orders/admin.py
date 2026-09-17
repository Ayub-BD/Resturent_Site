from django.contrib import admin

from .models import Order, OrderItem, OrderStatusHistory, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ("unit_price",)


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ("status", "changed_by", "timestamp")
    can_delete = False


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "table", "status", "total", "payment_method", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("order_number", "table__table_number")
    readonly_fields = ("order_number", "subtotal", "total")
    inlines = [OrderItemInline, PaymentInline, OrderStatusHistoryInline]
