from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),

    path("menu/", views.menu_manage, name="dashboard_menu"),
    path("menu/item/add/", views.menu_item_add, name="dashboard_menu_item_add"),
    path("menu/item/<int:item_id>/edit/", views.menu_item_edit, name="dashboard_menu_item_edit"),
    path("menu/item/<int:item_id>/delete/", views.menu_item_delete, name="dashboard_menu_item_delete"),
    path("menu/category/<int:category_id>/edit/", views.menu_category_edit, name="dashboard_menu_category_edit"),
    path("menu/category/<int:category_id>/toggle/", views.menu_category_toggle, name="dashboard_menu_category_toggle"),
    path("menu/category/<int:category_id>/delete/", views.menu_category_delete, name="dashboard_menu_category_delete"),

    path("tables/", views.table_manage, name="dashboard_tables"),
    path("tables/add/", views.table_add, name="dashboard_table_add"),
    path("tables/<int:table_id>/edit/", views.table_edit, name="dashboard_table_edit"),
    path("tables/<int:table_id>/set-status/", views.table_set_status, name="dashboard_table_set_status"),
    path("tables/<int:table_id>/delete/", views.table_delete, name="dashboard_table_delete"),

    path("reservations/", views.reservation_list, name="dashboard_reservations"),
    path("reservations/<int:reservation_id>/update/", views.reservation_update, name="dashboard_reservation_update"),

    path("offers/", views.offer_manage, name="dashboard_offers"),
    path("offers/add/", views.offer_add, name="dashboard_offer_add"),
    path("offers/<int:offer_id>/edit/", views.offer_edit, name="dashboard_offer_edit"),
    path("offers/<int:offer_id>/delete/", views.offer_delete, name="dashboard_offer_delete"),

    path("reviews/", views.review_manage, name="dashboard_reviews"),
    path("reviews/add/", views.review_add, name="dashboard_review_add"),
    path("reviews/<int:review_id>/approve/", views.review_approve, name="dashboard_review_approve"),
    path("reviews/<int:review_id>/reject/", views.review_reject, name="dashboard_review_reject"),
    path("reviews/<int:review_id>/delete/", views.review_delete, name="dashboard_review_delete"),

    path("orders/", views.order_list, name="dashboard_orders"),
    path("orders/new/", views.pos_start, name="dashboard_pos_start"),
    path("orders/<str:order_number>/", views.order_detail, name="dashboard_order_detail"),
    path("orders/<str:order_number>/receipt/", views.print_receipt, name="print_receipt"),
    path("orders/<str:order_number>/kitchen-ticket/", views.print_kitchen_ticket, name="print_kitchen_ticket"),
]
