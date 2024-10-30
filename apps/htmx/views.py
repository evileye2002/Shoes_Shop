import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http.response import HttpResponse

from apps.base_account.forms import (
    ChangePasswordForm,
    PasswordSetForm,
    UpdateProfileForm,
    UpdateContactForm,
    UpdateAvatarForm,
    AddAddressForm,
    UpdateAddressForm,
    UserAddress,
)


# Create your views here.
def change_password(request):

    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        hx_trigger = None

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Đổi mật khẩu thành công.")
            hx_trigger = {
                "updateModals": {
                    "close": ["change-password-modal"],
                }
            }

        ctx = {"form": form}
        response = render(request, "htmx/change_password.html", ctx)
        if hx_trigger:
            response["HX-Trigger"] = json.dumps(hx_trigger)
        return response

    return HttpResponse(status=204)


def set_password(request):

    if request.method == "POST":
        form = PasswordSetForm(request.user, request.POST)
        hx_trigger = None

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            form = ChangePasswordForm(user=request.user)
            messages.success(request, "Đổi mật khẩu thành công.")
            hx_trigger = {
                "updateModals": {
                    "close": ["change-password-modal"],
                }
            }

        ctx = {"form": form}
        response = render(request, "htmx/change_password.html", ctx)
        if hx_trigger:
            response["HX-Trigger"] = json.dumps(hx_trigger)
        return response

    return HttpResponse(status=204)


def update_info(request):
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật hồ sơ thành công.")

        ctx = {"form": form}
        return render(request, "htmx/update_info.html", ctx)

    return HttpResponse(status=204)


def update_contact(request):
    if request.method == "POST":
        form = UpdateContactForm(request.POST, instance=request.user)
        hx_trigger = None

        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật thông tin liên hệ thành công.")
            hx_trigger = {
                "updateModals": {
                    "close": ["update-contact-modal"],
                }
            }

        ctx = {"form": form}
        response = render(request, "htmx/update_contact.html", ctx)
        if hx_trigger:
            response["HX-Trigger"] = json.dumps(hx_trigger)
        return response

    return HttpResponse(status=204)


def update_avatar(request):
    if request.method == "POST":
        form = UpdateAvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật avatar thành công.")

        ctx = {"form": form}
        response = render(request, "htmx/update_avatar.html", ctx)
        response["HX-Trigger"] = json.dumps(
            {
                "updateModals": {
                    "close": ["update-avatar-modal"],
                }
            }
        )
        return response

    return HttpResponse(status=204)


def add_address(request):
    if request.method == "POST":
        form_add = AddAddressForm(request.POST)
        user_address = UserAddress.objects.filter(user=request.user)

        if form_add.is_valid():
            address = form_add.save(commit=False)
            address.user = request.user
            address.save()

            form_add = AddAddressForm()
            messages.success(request, "Thêm địa chỉ thành công.")

        ctx = {
            "type": "add",
            "form_add": form_add,
            "user_address": user_address,
        }
        return render(request, "htmx/update_address.html", ctx)

    return HttpResponse(status=204)


def update_address(request, id):
    address = get_object_or_404(UserAddress, id=id)
    form_update = UpdateAddressForm(instance=address)

    if request.method == "POST":
        form_update = UpdateAddressForm(
            request.POST,
            instance=address,
        )
        user_address = UserAddress.objects.filter(user=request.user)

        if form_update.is_valid():
            form_update.save()

            form_add = AddAddressForm()
            messages.success(request, "Cập nhật địa chỉ thành công.")
            ctx = {
                "type": "update",
                "form_update": form_update,
                "form_add": form_add,
                "user_address": user_address,
            }
            response = render(request, "htmx/update_address.html", ctx)
            response["HX-Trigger"] = json.dumps(
                {
                    "updateModals": {
                        "close": ["update-address-modal"],
                    }
                }
            )
            return response
        else:
            return HttpResponse(status=204)

    ctx = {"form_update": form_update}
    return render(request, "htmx/update_address_form.html", ctx)


def delete_address(request, id):
    address = get_object_or_404(UserAddress, id=id)
    address.delete()
    messages.success(request, "Xóa địa chỉ thành công.")

    form_add = AddAddressForm()
    user_address = UserAddress.objects.filter(user=request.user)

    ctx = {
        "type": "delete",
        "form_add": form_add,
        "user_address": user_address,
    }

    response = render(request, "htmx/update_address.html", ctx)
    response["HX-Trigger"] = json.dumps(
        {
            "updateModals": {
                "close": ["update-address-modal"],
            }
        }
    )
    return response


# Core
from django.http import HttpResponse, Http404
from django.db.models import (
    Avg,
    F,
    Count,
    Prefetch,
)

from apps.core.filters import ShoeFilter
from apps.core.enums import OrderStatus
from apps.core.forms import ReviewForm
from apps.core.models import (
    Shoe,
    Order,
    ShoppingCart,
    LineItem,
    ShoeOptionSize,
    ShoeOptionImage,
)
from apps.core.utils import (
    product_detail_handler,
    cart_item_total_price_handler,
    get_product_quantity_detail,
    get_lineitem_queryset,
    get_shoes_queryset,
    get_paginator,
)


def product_selection_update(request, uuid):
    shoe = (
        Shoe.objects.filter(uuid=uuid)
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

    previous_color = request.GET.get("previous-color")
    selected_color_uuid = request.GET.get("color")
    selected_size_uuid = request.GET.get("size")

    change_color = previous_color != selected_color_uuid
    quantity_detail = get_product_quantity_detail(shoe)
    product_detail = product_detail_handler(
        shoe,
        selected_color_uuid,
        selected_size_uuid if not change_color else None,
    )

    context = {
        "change_color": change_color,
        **product_detail,
        **quantity_detail,
    }
    return render(request, "htmx/product_selection_update.html", context)


def product_action(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        option_uuid = post_data.get("selected-option-size")
        shoe_option_size = get_object_or_404(ShoeOptionSize, uuid=option_uuid)
        quantity = int(post_data.get("quantity", 1))
        action = post_data.get("action")

        if quantity > 0 and shoe_option_size.quantity < quantity:
            messages.error(request, "Số lượng sản phẩm không hợp lệ.")
            return HttpResponse(status=204)

        if action == "add-to-cart":
            cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
            item, item_created = LineItem.objects.get_or_create(
                cart=cart,
                shoe_option_size=shoe_option_size,
                defaults={"quantity": quantity},
            )

            if not item_created:
                item.quantity = F("quantity") + quantity
                item.save()

            messages.success(request, "Thêm vào giỏ hàng thành công.")

    return render(request, "htmx/product_action.html")


def cart_item_action(request, uuid):
    cart = get_object_or_404(ShoppingCart, user=request.user)
    item = LineItem.objects.filter(uuid=uuid, cart=cart).first()

    if not item:
        return Http404()

    change_total_price = False
    checked_change = False
    change_quantity = False
    delete_item = False
    action = request.GET.get("action")
    item_checked = request.GET.get("item-checked", "off")
    selected_item_uuids = request.GET.getlist("selected-item-uuid", [])

    if action == "checked-change":
        change_total_price = True
        checked_change = True
        if item_checked == "on":
            selected_item_uuids.append(item.uuid)
        elif item.uuid in selected_item_uuids:
            selected_item_uuids.remove(item.uuid)

    if request.method == "POST":
        post_data = request.POST.copy()
        action = post_data.get("action")
        item_checked = post_data.get("item-checked", "off")
        item_quantity = int(post_data.get("item-quantity", 1))
        selected_item_uuids = post_data.getlist("selected-item-uuid", [])
        change_total_price = item_checked == "on"

        if item_quantity > 0 and item.shoe_option_size.quantity < item_quantity:
            messages.error(request, "Số lượng sản phẩm không hợp lệ.")
            return HttpResponse(status=204)

        if action == "change-quantity":
            if change_total_price:
                selected_item_uuids.append(item.uuid)
                checked_change = True
            elif item.uuid in selected_item_uuids:
                selected_item_uuids.remove(item.uuid)
            change_quantity = True
            item.quantity = item_quantity
            item.save()

        if action == "delete-cart-item":
            if item.uuid in selected_item_uuids:
                selected_item_uuids.remove(item.uuid)
                change_total_price = True
            checked_change = True
            delete_item = True
            item.delete()
            messages.success(request, "Xóa sản phảm thành công.")

    selected_items = get_lineitem_queryset(cart, selected_item_uuids)
    cart_items_data = cart_item_total_price_handler(list(selected_items))

    context = {
        "item": item,
        "change_total_price": change_total_price,
        "checked_change": checked_change,
        "change_quantity": change_quantity,
        "delete_item": delete_item,
        **cart_items_data,
    }
    return render(request, "htmx/cart_item_action.html", context)


def order_action(request):
    uuid = request.GET.get("order-uuid")
    action = request.GET.get("action")

    if action == "search":
        order = Order.objects.filter(uuid=uuid).first()
        if not order:
            messages.error(request, "Đơn hàng không tồn tại.")
            return HttpResponse(status=204)

    if request.method == "POST":
        post_data = request.POST.copy()
        post_uuid = post_data.get("order-uuid")
        action = post_data.get("action")

        order = Order.objects.filter(uuid=post_uuid, user=request.user).first()
        if not order:
            messages.error(request, "Đơn hàng không tồn tại.")
            return HttpResponse(status=204)

        if action == "cancel-order" and order.status == OrderStatus.PREPARING:
            order.status = OrderStatus.CANNCELED
            order.save()
            messages.success(request, "Hủy đơn hàng thành công.")

        if action == "delivered" and order.status == OrderStatus.SHIPPED:
            order.status = OrderStatus.DELIVERED
            order.save()
            messages.success(request, "Xác nhận nhận hàng thành công.")

    context = {
        "order": order,
    }
    return render(request, "htmx/order_action.html", context)


def review_action(request):
    action = request.GET.get("action")
    shoe_uuid = request.GET.get("shoe-uuid")
    quantity_detail = {}
    is_update_review = False

    if action == "get-form":
        shoe = Shoe.objects.filter(uuid=shoe_uuid)
        if not shoe.exists():
            messages.error(request, "Sản phẩm không tồn tại.")
            return HttpResponse(status=204)
        quantity_detail = get_product_quantity_detail(shoe.first(), request.user)

    if request.method == "POST":
        post_data = request.POST.copy()
        shoe_uuid = post_data.get("shoe-uuid")

        shoe = Shoe.objects.filter(uuid=shoe_uuid)
        if not shoe.exists():
            messages.error(request, "Sản phẩm không tồn tại.")
            return HttpResponse(status=204)

        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.shoe = shoe.first()
            new_review.user = request.user
            new_review.save()

            shoe = shoe.annotate(
                total_reviews=Count("reviews", distinct=True),
                avg_review=Avg("reviews__rating", distinct=True),
            ).values("total_reviews", "avg_review")

            is_update_review = True
            messages.success(request, "Đánh giá sản phẩm thành công.")

    context = {
        "shoe": shoe.first(),
        "is_update_review": is_update_review,
        "review_range": range(1, 6),
        **quantity_detail,
    }
    return render(request, "htmx/review_action.html", context)


def products_list(request):
    shoes_queryset = get_shoes_queryset(request)
    filter = ShoeFilter(request.GET, shoes_queryset)
    paginator = get_paginator(request, filter.qs)

    context = {
        "review_range": range(1, 6),
        "shoes": paginator,
    }
    return render(request, "htmx/products_list.html", context)


def product_reviews_list(request, uuid):
    shoe = get_object_or_404(Shoe, uuid=uuid)
    filter = ShoeFilter(request.GET, shoe.reviews.all())
    paginator = get_paginator(request, filter.qs, 5)

    context = {
        "review_range": range(1, 6),
        "reviews": paginator,
        "shoe_uuid": shoe.uuid,
    }
    return render(request, "htmx/product_reviews_list.html", context)
