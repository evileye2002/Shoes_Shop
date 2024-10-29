import os, random

from django.db import models
from django.core.management.base import BaseCommand

from apps.attribute.models import Category, Brand, Size, Color, Tag


class Command(BaseCommand):
    help = "Generate test Attributes"

    def handle(self, *args, **options):
        categories = [
            "Thể thao",
            "Thời trang",
            "Chạy bộ",
            "Dã ngoại",
        ]
        brands = [
            "Nike",
            "Adidas",
            "Puma",
            "Converse",
            "Vans",
            "Kappa",
            "Ecko Unltd",
            "Superga",
            "Gucci",
            "New Balance",
            "MLB",
            "Reebok",
            "Supreme",
            "Fila",
            "Alexander McQueen",
            "Common Project",
            "Biti's",
            "Balenciaga",
            "Louis Vuitton",
            "Rick Owens",
            "Dior",
            "Skechers",
            "Asics",
            "Salomon",
            "Fendi",
        ]
        tags = [
            "Giày thể thao",
            "Giày chạy bộ",
            "Giày công sở",
            "Giày chunky",
            "Giày lười",
            "Giày đế cao su",
            "Giày nữ",
            "Giày nam",
            "Sneaker",
        ]
        sizes = ["36", "37", "38", "39", "40", "41", "42", "43", "44", "45"]
        colors = [
            {
                "name": "Đen",
                "hex_1": "#000000",
                "hex_2": "",
            },
            {
                "name": "Trắng",
                "hex_1": "#F3F4F6",
                "hex_2": "",
            },
            {
                "name": "Đỏ",
                "hex_1": "#FF0000",
                "hex_2": "",
            },
            {
                "name": "Xanh dương",
                "hex_1": "#0000FF",
                "hex_2": "",
            },
            {
                "name": "Vàng",
                "hex_1": "#FFFF00",
                "hex_2": "",
            },
            {
                "name": "Nâu/Be",
                "hex_1": "#64433C",
                "hex_2": "#E3D6CD",
            },
            {
                "name": "Đen/Xanh lá",
                "hex_1": "#000000",
                "hex_2": "#6ABF80",
            },
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
                hex_color_1=color["hex_1"],
                hex_color_2=color["hex_2"],
            )

        print("Size Generating...")
        for size in sizes:
            Size.objects.get_or_create(name=size)

        print("All done!")
