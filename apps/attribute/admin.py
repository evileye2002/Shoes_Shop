from django.contrib import admin

from .models import Category, Brand, Size, Color, Tag

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Tag)
