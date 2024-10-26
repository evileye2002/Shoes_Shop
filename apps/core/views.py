from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.conf import settings
from django.db.models import (
    Avg,
    Min,
    Max,
    Subquery,
    F,
    ExpressionWrapper,
    IntegerField,
    Count,
    OuterRef,
    Prefetch,
)

from .models import (
    Shoe,
    ShoppingCart,
    LineItem,
    ShoeOptionImage,
    ShoeOptionSize,
    ShoeOption,
)
from .utils import product_detail_handler, cart_item_total_price_handler


# Create your views here.
def home(request):
    return render(request, "core/home.html")


def products(request):
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
    shoes = (
        Shoe.objects.annotate(
            total_reviews=Count("reviews", distinct=True),
            avg_review=Avg("reviews__rating", distinct=True),
            min_price=Min("options__sizes__price"),
            max_discount=Subquery(max_discount_subquery),
        )
        .prefetch_related("tags", "options__images")
        .order_by("-created_at")
        .distinct()
    )

    context = {
        "shoes": shoes,
        "review_range": range(0, 5),
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "core/products.html", context)


def product(request, uuid):
    shoe = (
        Shoe.objects.filter(uuid=uuid)
        .annotate(
            total_reviews=Count("reviews"),
            avg_review=Avg("reviews__rating"),
        )
        .prefetch_related(
            Prefetch(
                "options__images",
                queryset=ShoeOptionImage.objects.all(),
                to_attr="prefetched_images",
            ),
            Prefetch(
                "options__sizes",
                queryset=ShoeOptionSize.objects.select_related("size"),
                to_attr="prefetched_sizes",
            ),
            "options__color",
        )
        .first()
    )

    if not shoe:
        return Http404()

    product_detail = product_detail_handler(shoe)

    context = {
        "last_crum": shoe.name,
        "review_range": range(0, 5),
        "shoe": shoe,
        **product_detail,
    }
    return render(request, "core/product.html", context)


def shopping_cart(request):
    cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
    items_data = list(
        (
            LineItem.objects.filter(cart=cart)
            .prefetch_related("shoe_option_size__shoe_option__images")
            .select_related(
                "shoe_option_size__shoe_option__shoe",
                "shoe_option_size__size",
                "shoe_option_size__shoe_option__color",
            )
        )
    )

    context = {
        "items_data": items_data,
    }
    return render(request, "core/shopping_cart.html", context)
