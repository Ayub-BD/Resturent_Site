from .models import RestaurantProfile


def restaurant_profile(request):
    """
    Makes `profile` available in every template without every single view
    having to fetch and pass it manually. base.html, navbar.html and
    footer.html all rely on this being present.
    """
    return {"profile": RestaurantProfile.load()}
