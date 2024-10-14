from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="vnpay_index"),
    path("payment", views.payment, name="vnpay_payment"),
    path("payment_ipn", views.payment_ipn, name="vnpay_payment_ipn"),
    path("payment_return", views.payment_return, name="vnpay_payment_return"),
    path("query", views.query, name="vnpay_query"),
    path("refund", views.refund, name="vnpay_refund"),
]
