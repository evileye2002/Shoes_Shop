from django.conf import settings


BREADCRUMB_NAME_MAP = {
    "detail": {
        "label": "Thông tin chi tiết",
        "url": False,
    },
    "profile_manager": {
        "label": "Quản lý tài khoản",
        "url": False,
    },
    "products": {
        "label": "Sản phẩm",
        "url": True,
    },
    "shopping_cart": {
        "label": "Giỏ hàng của bạn",
        "url": False,
    },
    "ordering": {
        "label": "Đặt hàng",
        "url": False,
    },
    "about_us": {
        "label": "Về chúng tôi",
        "url": False,
    },
}


def breadcrumbs(request):
    """Generate breadcrumbs from the current URL path"""
    path = request.path.strip("/").split("/")
    breadcrumb_list = []
    url = ""

    for i, part in enumerate(path):
        url += f"/{part}"
        breadcrumb_info = BREADCRUMB_NAME_MAP.get(part)

        if isinstance(breadcrumb_info, dict):
            label = breadcrumb_info["label"]
            breadcrumb_url = url if breadcrumb_info["url"] else None
        else:
            label = part.capitalize()
            breadcrumb_url = url

        if part == "detail":
            break

        breadcrumb_list.append(
            {
                "name": label,
                "url": breadcrumb_url,
            }
        )

    return {"breadcrumbs": breadcrumb_list}


def media_url(request):
    if not settings.DEBUG:
        url = f"https://res.cloudinary.com/{settings.CLOUDINARY_CLOUD_NAME}/image/upload/v1/"
    else:
        url = settings.MEDIA_URL

    return {"media_url": url}
