from django.shortcuts import render, get_object_or_404

from .models import Shoe, ShoppingCart, LineItem
from .utils import product_detail_handler


# Create your views here.
def home(request):
    return render(request, "core/home.html")


def products(request):
    shoes = Shoe.objects.prefetch_related("options", "reviews")
    shoe_data = []
    max_discount = 0
    min_price = float("inf")
    review_avg = 0.0
    review_count = 0

    for shoe in shoes:
        options = list(shoe.options.all())
        reviews = list(shoe.reviews.all())

        if options:
            for option in options:
                min_price = min(min_price, option.price)
                if option.old_price is not None and option.old_price > 0:
                    discount_percentage = round(
                        (option.old_price - option.price) / option.old_price * 100, 0
                    )
                    max_discount = max(max_discount, discount_percentage)
        if reviews:
            review_avg = sum(review.rating for review in reviews) / len(reviews)
            review_count = len(reviews)

        shoe_data.append(
            {
                "shoe": shoe,
                "min_price": min_price,
                "review_range": range(0, 5),
                "review_avg": round(review_avg, 1),
                "review_avg_int": int(review_avg),
                "review_count": review_count,
                "max_discount": max_discount,
            }
        )

    if min_price == float("inf"):
        min_price = 0

    context = {"shoe_data": shoe_data}
    return render(request, "core/products.html", context)


def product(request, uuid):
    shoe = get_object_or_404(Shoe, uuid=uuid)
    selected_color = request.GET.get("color")
    selected_size = request.GET.get("size")
    product_data = product_detail_handler(shoe, selected_color, selected_size)

    context = {
        "last_crum": shoe.name,
        "shoe": shoe,
        **product_data,
    }
    return render(request, "core/product.html", context)


def shopping_cart(request):
    cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
    items = LineItem.objects.filter(cart=cart)

    context = {
        "items": items,
    }
    return render(request, "core/shopping_cart.html", context)
