from django.db import models


class Reservation(models.Model):
    """A table booking request submitted through the public site."""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_COMPLETED, "Completed"),
    ]

    # Linked automatically if we can match by email/phone; stays optional
    # because a customer can reserve without ever having an account.
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reservations",
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField(default=2)
    special_request = models.TextField(blank=True)

    table = models.ForeignKey(
        "tables.RestaurantTable",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reservations",
        help_text="Assigned by the manager after reviewing the request.",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.name} - {self.date} {self.time} ({self.guests} guests)"
