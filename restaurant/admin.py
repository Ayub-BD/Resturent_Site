from django.contrib import admin

from .models import Chef, ContactMessage, HistoryMilestone, RestaurantHistory, RestaurantProfile


@admin.register(RestaurantProfile)
class RestaurantProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "updated_at")

    def has_add_permission(self, request):
        # Singleton: block adding a second row from the admin UI.
        return not RestaurantProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class HistoryMilestoneInline(admin.TabularInline):
    model = HistoryMilestone
    extra = 1


@admin.register(RestaurantHistory)
class RestaurantHistoryAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    inlines = [HistoryMilestoneInline]

    def has_add_permission(self, request):
        return not RestaurantHistory.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "specialty", "experience_years", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "specialty")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
