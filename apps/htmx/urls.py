from django.urls import path
from . import views

urlpatterns = [
    path("change_password", views.change_password, name="htmx_change_password"),
    path("set_password", views.set_password, name="htmx_set_password"),
    path("update_info", views.update_info, name="htmx_update_info"),
    path("update_contact", views.update_contact, name="htmx_update_contact"),
    path("update_avatar", views.update_avatar, name="htmx_update_avatar"),
    path("add_address", views.add_address, name="htmx_add_address"),
    path("update_address/<str:id>", views.update_address, name="htmx_update_address"),
    path("delete_address/<str:id>", views.delete_address, name="htmx_delete_address"),
    # Core
    path(
        "product_selection_update/<str:uuid>",
        views.product_selection_update,
        name="htmx_product_selection_update",
    ),
    path("product_action", views.product_action, name="htmx_product_action"),
    path("order_action", views.order_action, name="htmx_order_action"),
    path(
        "cart_item_action/<str:uuid>",
        views.cart_item_action,
        name="htmx_cart_item_action",
    ),
    path("review_action", views.review_action, name="htmx_review_action"),
]
