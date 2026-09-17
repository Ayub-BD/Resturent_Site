from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("restaurant.urls")),
    path("menu/", include("menu.urls")),
    path("reserve/", include("reservations.urls")),
    path("order-now/", include("orders.urls")),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
]

if settings.DEBUG:
    # Serves uploaded media (chef photos, menu images, etc.) during development.
    # In production this is handled by the web server (nginx/etc.), not Django.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
