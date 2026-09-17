from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    path("login/", LoginView.as_view(template_name="dashboard_login.html"), name="dashboard_login"),
    path("logout/", LogoutView.as_view(), name="dashboard_logout"),
]
