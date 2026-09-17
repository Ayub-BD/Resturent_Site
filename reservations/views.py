from django.contrib import messages
from django.shortcuts import redirect, render

from customers.models import Customer

from .forms import ReservationForm


def reserve(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)

            # Link to an existing Customer by email if we recognize them,
            # otherwise create a new Customer record. Keeps the dashboard's
            # customer list building up automatically over time.
            customer, _created = Customer.objects.get_or_create(
                email=reservation.email,
                defaults={"name": reservation.name, "phone": reservation.phone},
            )
            reservation.customer = customer
            reservation.save()

            messages.success(
                request,
                "Your reservation request has been received! We'll confirm shortly.",
            )
            return redirect("reserve")
    else:
        form = ReservationForm()

    return render(request, "site/reserve.html", {"form": form})
