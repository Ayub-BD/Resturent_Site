from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from menu.models import MenuItem, Offer
from reviews.models import Review

from .forms import ContactForm
from .models import Chef, RestaurantHistory


def landing(request):
    """
    The very first page a visitor sees: choose to continue as a customer
    (goes to the normal public site) or log in as a manager (goes to the
    staff dashboard, behind manager_required).
    """
    return render(request, "site/landing.html")


def home(request):
    history = RestaurantHistory.load()
    chefs = Chef.objects.filter(is_active=True)
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:6]

    # is_currently_active combines the manual toggle + date range, so we
    # filter in Python rather than in the DB query.
    active_offers = [offer for offer in Offer.objects.filter(is_active=True) if offer.is_currently_active]

    approved_reviews = Review.objects.filter(is_approved=True)[:10]

    context = {
        "history": history,
        "chefs": chefs,
        "featured_items": featured_items,
        "active_offers": active_offers,
        "approved_reviews": approved_reviews,
    }
    return render(request, "site/home.html", context)


def our_story(request):
    history = RestaurantHistory.load()
    return render(request, "site/our_story.html", {"history": history})


def chef_detail(request, chef_id):
    chef = get_object_or_404(Chef, pk=chef_id, is_active=True)
    return render(request, "site/chef_detail.html", {"chef": chef})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out -- we'll get back to you soon.")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "site/contact.html", {"form": form})
