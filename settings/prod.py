import os, site, dj_database_url

from .base import *


SECRET_KEY = env("SECRET_KEY", default=SECRET_KEY)
DEBUG = False
ALLOWED_HOSTS = [".vercel.app", ".now.sh"]

INSTALLED_APPS += [
    "cloudinary_storage",
    "cloudinary",
]

# Crispy-form
site_packages = site.getsitepackages()[0]
is_set_site_packages = os.environ.get("Site_Packages")
if not is_set_site_packages:
    os.environ["Site_Packages"] = site_packages
    print("Set Site_Packages:", site_packages)

# Django-ckeditor-5
CKEDITOR_5_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# PostgresSQL database
db_url = env("DATABASE_URL")
DATABASES["default"] = dj_database_url.parse(db_url)

# Django-Cloudinary-Storage
CLOUDINARY_CLOUD_NAME = env("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = env("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = env("CLOUDINARY_API_SECRET")
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
    "API_KEY": CLOUDINARY_API_KEY,
    "API_SECRET": CLOUDINARY_API_SECRET,
}
STORAGES = {
    "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
