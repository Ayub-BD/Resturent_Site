from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "rating", "is_approved", "created_at")
    list_editable = ("is_approved",)
    list_filter = ("is_approved", "rating")
    search_fields = ("customer_name", "comment")
    actions = ["approve_reviews", "reject_reviews"]

    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Reject (unapprove) selected reviews")
    def reject_reviews(self, request, queryset):
        queryset.update(is_approved=False)
