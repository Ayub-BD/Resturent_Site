from django import forms

from .models import MenuCategory, MenuItem, Offer

INPUT_CLASS = "form-control"


class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ["name", "display_order", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "e.g. Burgers"}),
            "display_order": forms.NumberInput(attrs={"class": INPUT_CLASS}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # New categories should be visible on the site by default -- previously
        # this checkbox wasn't rendered anywhere, so every new category silently
        # saved as inactive (is_active=False) and never showed up on the menu.
        if not self.instance.pk:
            self.fields["is_active"].initial = True


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            "category", "name", "description", "price", "old_price",
            "image", "is_available", "is_featured",
        ]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASS, "rows": 3}),
            "price": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
            "old_price": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            "title", "description", "image", "discount_percent",
            "start_date", "end_date", "is_active",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASS, "rows": 3}),
            "discount_percent": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 1, "max": 100}),
            "start_date": forms.DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
        }
