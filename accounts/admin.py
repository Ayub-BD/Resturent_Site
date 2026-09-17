from django.contrib import admin

from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone", "is_active_staff")
    list_filter = ("role", "is_active_staff")
    search_fields = ("user__username", "user__first_name", "user__last_name", "phone")
