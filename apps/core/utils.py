from decimal import Decimal

from django.core.paginator import Paginator

from .models import LineItem

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


def product_detail_handler(
    shoe,
    selected_option_uuid=None,
    selected_option_size_uuid=None,
):
    options = list(shoe.options.all())
    all_sizes = list(
        {
            size.size: size for option in options for size in option.prefetched_sizes
        }.values()
    )

    selected_option = (
        options[0]
        if selected_option_uuid is None
        else next(
            (option for option in options if option.uuid == selected_option_uuid), None
        )
    )
    selected_option_images = selected_option.prefetched_images
    selected_option_sizes = sorted(
        {size for size in selected_option.prefetched_sizes if size.quantity > 0},
        key=lambda size: int(size.size.name),
    )
    all_sizes = sorted(
        {size for size in selected_option.prefetched_sizes},
        key=lambda size: int(size.size.name),
    )

    selected_size = (
        selected_option_sizes[0]
        if selected_option_size_uuid is None
        else next(
            (
                size
                for size in selected_option_sizes
                if size.uuid == selected_option_size_uuid
            ),
            None,
        )
    )

    selected_size_discount = (
        round(
            (selected_size.old_price - selected_size.price)
            / selected_size.old_price
            * 100,
            0,
        )
        if selected_size.old_price and selected_size.old_price > 0
        else 0
    )

    context = {
        "options": options,
        "all_sizes": all_sizes,
        "selected_option_images": selected_option_images,
        "selected_option_sizes": selected_option_sizes,
        "selected_option": selected_option,
        "selected_size": selected_size,
        "selected_size_discount": selected_size_discount,
    }

    return context


def cart_item_total_price_handler(cart, selected_item_uuids=[], prefetch_related=False):
    items = LineItem.objects.filter(
        cart=cart,
        uuid__in=selected_item_uuids,
    )
    selected_items = (
        list(items)
        if not prefetch_related
        else list(
            items.prefetch_related(
                "shoe_option_size__shoe_option__images"
            ).select_related(
                "shoe_option_size__shoe_option__shoe",
                "shoe_option_size__size",
                "shoe_option_size__shoe_option__color",
            )
        )
    )

    total_item_price = sum(data.get_total_price() for data in selected_items)
    tax = total_item_price * Decimal("0.1")
    total_price = total_item_price + tax
    saving = sum(data.get_total_old_price() for data in selected_items) - total_price

    return {
        "selected_items": selected_items,
        "total_item_price": total_item_price,
        "tax": tax,
        "total_price": total_price,
        "saving": saving if saving > 0 else 0,
    }
