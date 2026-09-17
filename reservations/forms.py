from django import forms

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["name", "email", "phone", "date", "time", "guests", "special_request"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "guests": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "special_request": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Optional"}
            ),
        }
