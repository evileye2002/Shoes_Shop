import site, dj_database_url

from .base import *


DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "django_browser_reload",
    "debug_toolbar",
]

MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "settings.urls.dev"

INTERNAL_IPS = [
    "127.0.0.1",
]

# Django-Tailwind
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"


# PostgresSQL database
db_url = env("DATABASE_URL")
DATABASES["default"] = dj_database_url.parse(db_url)


# Crispy-form
site_packages = os.path.join(site.getsitepackages()[0], "Lib", "site-packages")
is_set_site_packages = os.environ.get("Site_Packages")
if not is_set_site_packages:
    os.environ["Site_Packages"] = site_packages
    print("Set Site_Packages:", site_packages)


# Django-ckeditor-5
CKEDITOR_5_FILE_STORAGE = "apps.core.storage.CustomStorage"
