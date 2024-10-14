from .base import *
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns += [
    path("__reload__/", include("django_browser_reload.urls")),
] + debug_toolbar_urls()
