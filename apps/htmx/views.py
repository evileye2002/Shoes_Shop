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
from django.db.models import F

from apps.core.models import Shoe, ShoeOption, ShoppingCart, LineItem
from apps.core.utils import product_detail_handler


def product_price(request, uuid):
    shoe = get_object_or_404(Shoe, uuid=uuid)
    previous_color = request.GET.get("previous-color")
    selected_color = request.GET.get("color")
    selected_size = request.GET.get("size")
    change_color = previous_color != selected_color
    product_data = product_detail_handler(shoe, selected_color, selected_size)

    context = {
        "change_color": change_color,
        **product_data,
    }
    return render(request, "htmx/product_price.html", context)


def product_action(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        option_uuid = post_data.get("selected-option")
        shoe_option = get_object_or_404(ShoeOption, uuid=option_uuid)
        quantity = int(post_data.get("quantity", 1))
        action = post_data.get("action")

        if action == "add-to-cart" and quantity > 0:
            cart, created = ShoppingCart.objects.get_or_create(user=request.user)
            item, item_created = LineItem.objects.get_or_create(
                cart=cart, shoe_option=shoe_option, defaults={"quantity": quantity}
            )

            if not item_created:
                item.quantity = F("quantity") + quantity
                item.save()

            messages.success(request, "Thêm vào giỏ hàng thành công.")

    return HttpResponse(status=204)
