from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["customer_name", "email", "rating", "comment", "photo", "is_approved"]
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
