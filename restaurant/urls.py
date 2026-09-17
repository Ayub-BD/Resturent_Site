from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("home/", views.home, name="home"),
    path("our-story/", views.our_story, name="our_story"),
    path("chef/<int:chef_id>/", views.chef_detail, name="chef_detail"),
    path("contact/", views.contact, name="contact"),
]
