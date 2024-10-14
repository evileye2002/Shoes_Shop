from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("apps.base_account.urls")),
    path("htmx/", include("apps.htmx.urls")),
    path("vnpay/", include("apps.vnpay.urls")),
    path("social_account/", include("allauth.urls")),
    path("", include("apps.core.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
