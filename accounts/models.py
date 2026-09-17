from django.contrib.auth.models import User
from django.db import models


class Staff(models.Model):
    """
    Extends Django's built-in User with restaurant-specific role info.
    Every dashboard/kitchen/POS user (manager, waiter, kitchen staff)
    has a linked Staff profile. Plain customers do NOT get a User account
    at all -- they interact anonymously (reviews, reservations, orders
    just store their name/email/phone directly).
    """

    ROLE_MANAGER = "manager"
    ROLE_WAITER = "waiter"
    ROLE_KITCHEN = "kitchen"

    ROLE_CHOICES = [
        (ROLE_MANAGER, "Manager"),
        (ROLE_WAITER, "Waiter"),
        (ROLE_KITCHEN, "Kitchen Staff"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_WAITER)
    phone = models.CharField(max_length=20, blank=True)
    is_active_staff = models.BooleanField(
        default=True,
        help_text="Deactivate to revoke dashboard access without deleting the account.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    @property
    def is_manager(self):
        return self.role == self.ROLE_MANAGER

    @property
    def is_waiter(self):
        return self.role == self.ROLE_WAITER

    @property
    def is_kitchen(self):
        return self.role == self.ROLE_KITCHEN
