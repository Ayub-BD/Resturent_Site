from django import forms

from .models import RestaurantTable

INPUT_CLASS = "form-control"


class RestaurantTableForm(forms.ModelForm):
    class Meta:
        model = RestaurantTable
        fields = ["table_number", "capacity", "status"]
        widgets = {
            "table_number": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "e.g. T-05"}),
            "capacity": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 1}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
