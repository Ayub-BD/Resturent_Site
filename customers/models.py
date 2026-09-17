from django.db import models


class Customer(models.Model):
    """
    A known customer record, built up over time from reservations/orders.
    Order count / total spend / last order are computed on demand (see
    properties below) rather than stored, so they can never drift out of
    sync with the actual Order records.
    """

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def order_count(self):
        return self.orders.filter(status="completed").count()

    @property
    def total_spent(self):
        from django.db.models import Sum

        total = self.orders.filter(status="completed").aggregate(total=Sum("total"))["total"]
        return total or 0

    @property
    def last_order(self):
        return self.orders.order_by("-created_at").first()
