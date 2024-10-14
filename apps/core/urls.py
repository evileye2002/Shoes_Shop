from django.urls import path, include
from apps.core import views

urlpatterns = [
    path("", views.home, name="home"),
]
