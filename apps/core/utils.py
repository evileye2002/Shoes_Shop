from django.core.paginator import Paginator


ITEM_PER_PAGE = 12


def format_number_with_commas(value):
    value_str = "{:,}".format(int(value))
    return value_str


def format_datetime_vn(value):
    day = value.strftime("%d")
    month = f"Tháng {value.month}"
    year = value.strftime("%Y")
    time = value.strftime("%H:%M")
    return f"{time}, {day} {month} {year}"


def get_paginator(request, queryset, item_per_page=ITEM_PER_PAGE):
    if queryset.count() < item_per_page:
        return queryset

    p = Paginator(queryset, item_per_page)
    page = request.GET.get("page")
    return p.get_page(page)


def product_detail_handler(shoe, selected_color, selected_size, query_all=True):
    if query_all:
        reviews = list(shoe.reviews.all())
        options = list(
            shoe.options.select_related("color", "size").prefetch_related("images")
        )
    else:
        reviews = None
        options = list(shoe.options.select_related("color", "size"))

    discount = 0
    review_avg = 0.0
    review_count = 0
    option_images = []
    colors = set()
    sizes = set()

    if reviews:
        review_avg = sum(review.rating for review in reviews) / len(reviews)
        review_count = len(reviews)

    for option in options:
        if query_all:
            option_images.extend(option.images.all())
        if option.color:
            colors.add(option.color)
        if option.size:
            sizes.add(option.size)

    sizes = sorted(sizes, key=lambda size: size.name)

    available_colors = sorted(
        {str(option.color.id) for option in options if option.quantity > 0}
    )
    selected_color = selected_color or available_colors[0]

    selected_options = [
        option
        for option in options
        if option.color.id == int(selected_color) and option.quantity > 0
    ]

    available_sizes = sorted(
        {
            str(option.size.id)
            for option in selected_options
            if option.size and option.quantity > 0
        },
    )
    selected_size = (
        selected_size if selected_size in available_sizes else available_sizes[0]
    )

    selected_options = [
        option for option in selected_options if option.size.id == int(selected_size)
    ]

    if (
        selected_options
        and selected_options[0].old_price
        and selected_options[0].old_price > 0
    ):
        discount = round(
            (selected_options[0].old_price - selected_options[0].price)
            / selected_options[0].old_price
            * 100,
            0,
        )

    context = {
        "colors": colors,
        "sizes": sizes,
        "selected_color": selected_color,
        "selected_size": selected_size,
        "selected_options": selected_options,
        "discount": discount,
        "available_colors": available_colors,
        "available_sizes": available_sizes,
        "option_images": option_images,
        "review_range": range(0, 5),
        "review_avg": round(review_avg, 1),
        "review_avg_int": int(review_avg),
        "review_count": review_count,
    }
    return context
