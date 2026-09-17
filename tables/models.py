from django.db import models


class RestaurantTable(models.Model):
    """A physical table in the restaurant, tracked for both reservations and POS orders."""

    STATUS_AVAILABLE = "available"
    STATUS_OCCUPIED = "occupied"
    STATUS_RESERVED = "reserved"
    STATUS_CLEANING = "cleaning"

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, "Available"),
        (STATUS_OCCUPIED, "Occupied"),
        (STATUS_RESERVED, "Reserved"),
        (STATUS_CLEANING, "Cleaning"),
    ]

    table_number = models.CharField(max_length=10, unique=True, help_text="e.g. T-05")
    capacity = models.PositiveIntegerField(default=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE
    )

    class Meta:
        ordering = ["table_number"]

    def __str__(self):
        return f"{self.table_number} ({self.get_status_display()})"
