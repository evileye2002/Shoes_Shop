from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Avg, Count, Prefetch
from apps.vnpay.utils import create_payment, payment_return_handler
from apps.attribute.models import Color, Size

from .models import (
    Shoe,
    ShoppingCart,
    LineItem,
    ShoeOptionImage,
    ShoeOptionSize,
    Payment,
    Order,
)
from .utils import (
    product_detail_handler,
    cart_item_total_price_handler,
    get_shoes_queryset,
    get_brands_group_by_alphabet,
    get_lineitem_queryset,
    get_product_quantity_detail,
    get_paginator,
)
from .forms import OrderForm
from .enums import PaymentMethods, OrderStatus
from .filters import ShoeFilter


# Create your views here.
def test(request):
    shoes = get_shoes_queryset(request)
    filter = ShoeFilter(request.GET, shoes)

    brands_group_by_alphabet = get_brands_group_by_alphabet()

    context = {
        "filter": filter,
    }
    return render(request, "test.html", context)


def home(request):
    return render(request, "core/home.html")


def products(request):
    shoes_queryset = get_shoes_queryset(request)
    brands_group_by_alphabet = get_brands_group_by_alphabet()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    filter = ShoeFilter(request.GET, shoes_queryset)
    paginator = get_paginator(request, filter.qs)

    context = {
        "review_range": range(1, 6),
        "shoes": paginator,
        "colors": colors,
        "sizes": sizes,
        **brands_group_by_alphabet,
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
            "reviews__user",
        )
        .first()
    )

    if not shoe:
        return Http404()

    quantity_detail = get_product_quantity_detail(shoe)
    product_detail = product_detail_handler(shoe)
    reviews_paginator = get_paginator(request, shoe.reviews.all(), 5)

    if not product_detail:
        return HttpResponse(status=404)

    context = {
        "last_crum": shoe.name,
        "review_range": range(1, 6),
        "shoe": shoe,
        "reviews": reviews_paginator,
        **product_detail,
        **quantity_detail,
    }
    return render(request, "core/product.html", context)


def shopping_cart(request):
    cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
    items_data = get_lineitem_queryset(cart, select_related=True)

    context = {
        "items_data": items_data,
    }
    return render(request, "core/shopping_cart.html", context)


def ordering(request):
    cart = get_object_or_404(ShoppingCart, user=request.user)
    selected_item_uuids = request.GET.getlist("siu", [])

    shipping_fee = 15000
    form = OrderForm(user=request.user)
    selected_items = get_lineitem_queryset(cart, selected_item_uuids, True)
    cart_items_data = cart_item_total_price_handler(selected_items)

    if len(cart_items_data["selected_items"]) == 0:
        return HttpResponse(status=404)

    total_order_price = shipping_fee + cart_items_data["total_price"]

    if request.method == "POST":
        post_data = request.POST.copy()
        action = post_data.get("action")

        if action == "checkout":
            # TODO: Check item quantity before checkout
            form = OrderForm(request.POST, user=request.user)
            if form.is_valid():
                payment_method = form.cleaned_data["payment_method"]
                order = form.save(commit=False)
                order.user = request.user
                order.total_payment = total_order_price
                order.save()
                for item in cart_items_data["selected_items"]:
                    item.order = order
                    item.save()

                redirect_url = (
                    f"/payment_return?vnp_ResponseCode=-1&vnp_TxnRef={order.uuid}"
                )
                if payment_method == PaymentMethods.ONLINE_PAYMENT:
                    redirect_url = create_payment(
                        request,
                        order.uuid,
                        order.total_payment,
                    )
                    # print("redirect_url", redirect_url)

                return redirect(redirect_url)

    context = {
        "form": form,
        "shipping_fee": shipping_fee,
        "total_order_price": total_order_price,
        **cart_items_data,
    }
    return render(request, "core/ordering.html", context)


def payment_return(request):
    res_code = request.GET.get("vnp_ResponseCode")
    order_id = request.GET.get("vnp_TxnRef")

    if not res_code or not order_id:
        return HttpResponse(status=404)

    response_data = {
        "res_code": res_code,
        "order_id": order_id,
    }

    order = get_object_or_404(
        Order,
        uuid=order_id,
        user=request.user,
    )

    success_code = ["-1", "00"]

    if not order.status == OrderStatus.PENDING or not res_code in success_code:
        return render(request, "core/payment_return.html", response_data)

    for item in order.items.all():
        item.cart = None
        item.save()

    if order.payment_method == PaymentMethods.CASH_ON_DELIVERY:
        order.status = OrderStatus.PREPARING
        order.save()

    if res_code == "00":
        response_data = {**payment_return_handler(request), **response_data}
        Payment.objects.create(
            order_id=response_data["order_id"],
            order_desc=response_data["order_desc"],
            amount=response_data["amount"],
            bank_code=response_data["bank_code"],
        )
        order.status = OrderStatus.PREPARING
        order.save()

    return render(request, "core/payment_return.html", response_data)
