from django.urls import path
from apps.core import views

urlpatterns = [
    path("", views.home, name="home"),
    path("test", views.test, name="test"),
    path("products", views.products, name="products"),
    path("products/detail/<str:uuid>", views.product, name="product"),
    path("shopping_cart", views.shopping_cart, name="shopping_cart"),
    path("ordering", views.ordering, name="ordering"),
    path("payment_return", views.payment_return, name="payment_return"),
]
