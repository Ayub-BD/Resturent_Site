from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    """A customer review submitted through the public site, pending manager approval."""

    customer_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    photo = models.ImageField(upload_to="reviews/", blank=True, null=True)

    is_approved = models.BooleanField(
        default=False, help_text="Only approved reviews appear on the public website."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.rating}/5"
