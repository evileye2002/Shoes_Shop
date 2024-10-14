from django.apps import AppConfig


class BaseAccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.base_account"
