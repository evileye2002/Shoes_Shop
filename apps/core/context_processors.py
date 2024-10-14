BREADCRUMB_NAME_MAP = {
    "account": "Tài khoản của bạn",
    "sign_in": "Đăng nhập",
    "đăng ký": "Đăng nhập",
    "profile_manager": "Quản lý tài khoản",
}


def breadcrumbs(request):
    """Generate breadcrumbs from the current URL path"""
    path = request.path.strip("/").split("/")
    breadcrumb_list = []
    url = ""

    for i, part in enumerate(path):
        url += f"/{part}"
        name = BREADCRUMB_NAME_MAP.get(
            part, part.capitalize()
        )  # Use mapping if available
        breadcrumb_list.append(
            {
                "name": name,
                "url": (
                    url if i != len(path) - 1 else None
                ),  # No link for the current page
            }
        )

    return {"breadcrumbs": breadcrumb_list}
