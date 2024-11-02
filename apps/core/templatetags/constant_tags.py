from django import template

register = template.Library()

NAVBAR_LINKS = [
    {"url": "/", "label": "Trang chủ"},
    {"url": "/products?o=newest", "label": "Sản phẩm mới"},
    {"url": "/products", "label": "Sản phẩm nổi bật"},
    {"url": "/about_us", "label": "Về chúng tôi"},
]

CONFIG = {
    "web_name": "Xuân Minh",
    "description": "Xuân Minh Shoes Description",
    "shortcute_icon": "/static/imgs/logo.svg",
    "copyright": "Xuân Minh Shoes. All Rights Reserved",
}


@register.simple_tag
def get_navbar_links():
    return NAVBAR_LINKS


@register.simple_tag
def get_config_settings():
    return CONFIG
