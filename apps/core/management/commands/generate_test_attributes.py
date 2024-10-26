import os, random

from django.db import models
from django.core.management.base import BaseCommand

from apps.attribute.models import Category, Brand, Size, Color, Tag


class Command(BaseCommand):
    help = "Generate test Attributes"

    def handle(self, *args, **options):
        categories = ["Thể thao", "Thời trang", "Chạy bộ", "Dã ngoại"]
        brands = [
            "Nike",
            "Adidas",
            "Puma",
            "Converse",
            "Vans",
            "Kappa",
        ]
        tags = [
            "Giày thể thao",
            "Sneaker",
            "Giày chạy bộ",
            "Hàng mới",
            "Sale",
        ]
        sizes = ["36", "37", "38", "39", "40", "41", "42", "43", "44", "45"]
        colors = [
            {"name": "Đen", "hex": "#000000"},
            {"name": "Trắng", "hex": "#FFFFFF"},
            {"name": "Đỏ", "hex": "#FF0000"},
            {"name": "Xanh dương", "hex": "#0000FF"},
            {"name": "Vàng", "hex": "#FFFF00"},
            {"name": "Nâu/Be", "hex": "#FFFF00"},
            {"name": "Đen/Xanh lá", "hex": "#FFFF00"},
        ]

        print("Attribute Generating...")

        print("Category Generating...")
        for category in categories:
            Category.objects.get_or_create(name=category)

        print("Brand Generating...")
        for brand in brands:
            Brand.objects.get_or_create(name=brand)

        print("Tag Generating...")
        for tag in tags:
            Tag.objects.get_or_create(name=tag)

        print("Color Generating...")
        for color in colors:
            Color.objects.get_or_create(
                name=color["name"],
                # hex_color=color["hex"],
            )

        print("Size Generating...")
        for size in sizes:
            Size.objects.get_or_create(name=size)

        print("All done!")
