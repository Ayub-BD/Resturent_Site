from django.urls import path

from . import views

urlpatterns = [
    path("", views.order_now, name="order_now"),
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/<int:item_id>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:item_id>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:item_id>/", views.cart_remove, name="cart_remove"),
    path("confirmation/<str:order_number>/", views.order_confirmation, name="order_confirmation"),
]
