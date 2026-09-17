from django.contrib import admin

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "time", "guests", "table", "status")
    list_editable = ("status",)
    list_filter = ("status", "date")
    search_fields = ("name", "email", "phone")
    date_hierarchy = "date"
