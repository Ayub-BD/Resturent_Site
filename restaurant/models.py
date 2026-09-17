from django.core.exceptions import ValidationError
from django.db import models


class RestaurantProfile(models.Model):
    """
    Singleton model -- there should only ever be ONE row in this table.
    Holds every site-wide setting the manager can edit from the dashboard,
    so nothing (Foodpanda URL, address, hours, etc.) is hard-coded in templates.
    """

    name = models.CharField(max_length=150, default="My Restaurant")
    logo = models.ImageField(upload_to="restaurant/", blank=True, null=True)
    tagline = models.CharField(max_length=200, blank=True)

    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    opening_hours = models.TextField(
        blank=True,
        help_text="e.g. Mon-Fri: 10am-11pm\nSat-Sun: 9am-12am",
    )

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    foodpanda_url = models.URLField(
        blank=True,
        help_text="Where the 'Order Now' button sends customers for delivery.",
    )
    google_maps_url = models.URLField(blank=True)

    about_text = models.TextField(blank=True)
    primary_color = models.CharField(
        max_length=7,
        default="#c0392b",
        help_text="Hex color, e.g. #c0392b. Drives the site's accent color via a CSS variable.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Restaurant Profile"
        verbose_name_plural = "Restaurant Profile"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Enforce singleton: always overwrite row with pk=1.
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Prevent accidental deletion of the only settings row.

    @classmethod
    def load(cls):
        """Fetch the single settings row, creating it with defaults if missing."""
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj


class RestaurantHistory(models.Model):
    """
    Singleton, like RestaurantProfile: the 'Our Story' page content.
    Milestones (the timeline) are a separate related model below.
    """

    title = models.CharField(max_length=150, default="Our Story")
    founder_story = models.TextField(blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="restaurant/history/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Restaurant History"
        verbose_name_plural = "Restaurant History"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj


class HistoryMilestone(models.Model):
    """One entry in the 'Our Story' timeline, e.g. '2015 - Restaurant founded'."""

    history = models.ForeignKey(
        RestaurantHistory, on_delete=models.CASCADE, related_name="milestones"
    )
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "year"]

    def __str__(self):
        return f"{self.year} - {self.title}"


class Chef(models.Model):
    """A single chef profile shown in the 'Our Chefs' section."""

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="chefs/", blank=True, null=True)
    designation = models.CharField(max_length=100, help_text="e.g. Executive Chef")
    specialty = models.CharField(max_length=150, help_text="e.g. Italian & Continental Cuisine")
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0, help_text="Years of experience")

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(
        default=True, help_text="Only active chefs appear on the public website."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.name} ({self.designation})"


class ContactMessage(models.Model):
    """A message submitted through the public contact form."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"
