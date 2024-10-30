from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import (
    F,
    Min,
    Sum,
    Avg,
    Count,
    Value,
    OuterRef,
    Subquery,
    IntegerField,
    ExpressionWrapper,
)
from django.db.models.functions import Coalesce
from apps.attribute.models import Brand
from .models import Shoe, ShoeOptionSize
from .models import LineItem, Order, Review, ShoeOptionImage
from .enums import OrderStatus, PRODUCT_ORDER_CHOICES

ITEM_PER_PAGE = 12
PAGE_QUERYSTRING = "page"


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
    page = request.GET.get(PAGE_QUERYSTRING)
    return p.get_page(page)


def get_product_quantity_detail(shoe, user=None):
    delivered_orders = Order.objects.filter(
        items__shoe_option_size__shoe_option__shoe=shoe,
        status=OrderStatus.DELIVERED,
    )
    total_solds = (
        delivered_orders.aggregate(total_solds=Sum("items__quantity"))["total_solds"]
        or 0
    )
    allow_user_review = False

    if user:
        time_threshold = timezone.now() - timedelta(hours=24)
        user_orders = delivered_orders.filter(user=user, updated_at__gte=time_threshold)
        user_reviews = Review.objects.filter(
            user=user, shoe=shoe, created_at__gte=time_threshold
        )

        if user_orders.count() > 0 and user_reviews.count() == 0:
            allow_user_review = True

        # TODO: Check user is review in 24h or not

    return {
        "total_solds": total_solds,
        "allow_user_review": allow_user_review,
    }


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
        if selected_option_uuid is None and options
        else next(
            (option for option in options if option.uuid == selected_option_uuid), None
        )
    )

    if selected_option is None:
        return {}

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


def cart_item_total_price_handler(selected_items):
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


def get_shoes_queryset(request):
    ordering = request.GET.get("o")
    order_by = PRODUCT_ORDER_CHOICES.get(ordering, "-avg_review")

    max_discount_subquery = (
        ShoeOptionSize.objects.filter(shoe_option__shoe=OuterRef("pk"))
        .annotate(
            discount=ExpressionWrapper(
                (F("old_price") - F("price")) / F("old_price") * 100,
                output_field=IntegerField(),
            )
        )
        .values("discount")
        .order_by("-discount")[:1]
    )

    first_image_subquery = ShoeOptionImage.objects.filter(
        shoe_option__shoe=OuterRef("pk")
    ).values("image")[:1]

    shoes = (
        Shoe.objects.annotate(
            total_reviews=Count("reviews", distinct=True),
            avg_review=Coalesce(Avg("reviews__rating"), Value(0.0)),
            min_price=Min("options__sizes__price"),
            max_discount=Coalesce(Subquery(max_discount_subquery), Value(0)),
            first_image_path=Subquery(first_image_subquery),
        )
        .prefetch_related(
            "tags",
            # "options__images",
        )
        .order_by(order_by)
        # .distinct()
    )

    return shoes


def get_brands_group_by_alphabet():
    brands = Brand.objects.prefetch_related("shoes").order_by("name")
    brands_alphabet = {}

    for brand in brands:
        first_char = brand.name[0]
        if first_char not in brands_alphabet:
            brands_alphabet[first_char] = []

        brands_alphabet[first_char].append(brand)

    return {"brands_alphabet": brands_alphabet}


def get_lineitem_queryset(cart, selected_item_uuids=None, select_related=False):
    if selected_item_uuids is not None:
        queryset = LineItem.objects.filter(cart=cart, uuid__in=selected_item_uuids)
    else:
        queryset = LineItem.objects.filter(cart=cart)

    if select_related:
        first_image_subquery = ShoeOptionImage.objects.filter(
            shoe_option=OuterRef("shoe_option_size__shoe_option__pk")
        ).values("image")[:1]

        queryset = queryset.annotate(
            shoe_uuid=F("shoe_option_size__shoe_option__shoe__uuid"),
            shoe_name=F("shoe_option_size__shoe_option__shoe__name"),
            option_size=F("shoe_option_size__size__name"),
            option_color=F("shoe_option_size__shoe_option__color__name"),
            option_quantity=F("shoe_option_size__quantity"),
            first_image_path=Subquery(first_image_subquery),
        ).select_related("shoe_option_size")

    return queryset
