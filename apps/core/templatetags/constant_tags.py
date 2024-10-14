from django import template
from django.shortcuts import resolve_url

register = template.Library()

NAVBAR_LINKS = [
    {"url": "/", "label": "Trang chủ"},
    {"url": "/products", "label": "Sản phẩm"},
    {"url": "/blogs", "label": "Bài viết"},
    {"url": "/about_us", "label": "Về chúng tôi"},
    {"url": "/contact", "label": "Liên hệ"},
]

CONFIG = {
    "web_name": "Django Staterkit",
    "description": "Django Staterkit Description",
    "shortcute_icon": "/static/imgs/logo.svg",
    "copyright": "Django Starterkit. All Rights Reserved",
}


@register.simple_tag
def get_navbar_links():
    return NAVBAR_LINKS


@register.simple_tag
def get_config_settings():
    return CONFIG
