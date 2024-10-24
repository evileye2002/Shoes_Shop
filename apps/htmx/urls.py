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
    path("product_price/<str:uuid>", views.product_price, name="htmx_product_price"),
    path("product_action", views.product_action, name="htmx_product_action"),
]
