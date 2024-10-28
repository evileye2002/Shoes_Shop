from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
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
    Payment,
    Order,
)
from .utils import product_detail_handler, cart_item_total_price_handler
from .forms import OrderForm
from .enums import PaymentMethods, OrderStatus
from apps.vnpay.utils import create_payment, payment_return_handler


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
        .prefetch_related("tags", "options__images", "reviews")
        .order_by("-created_at")
        .distinct()
    )

    context = {
        "shoes": shoes,
        "review_range": range(0, 5),
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
            "reviews",
            "reviews__user",
        )
        .first()
    )

    if not shoe:
        return Http404()

    product_detail = product_detail_handler(shoe, user=request.user)

    context = {
        "last_crum": shoe.name,
        "review_range": range(0, 5),
        "shoe": shoe,
        "reviews": shoe.reviews.all(),
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


def ordering(request):
    cart = get_object_or_404(ShoppingCart, user=request.user)
    selected_item_uuids = request.GET.getlist("siu", [])

    shipping_fee = 15000
    form = OrderForm(user=request.user)
    cart_items_data = cart_item_total_price_handler(
        cart,
        selected_item_uuids,
        True,
    )

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
                    item.cart = None
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
                elif payment_method == PaymentMethods.CASH_ON_DELIVERY:
                    order.status = OrderStatus.PREPARING
                    order.save()
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
