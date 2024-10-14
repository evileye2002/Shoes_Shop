from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (
    SignUpForm,
    SignInForm,
    ChangePasswordForm,
    PasswordSetForm,
    UpdateProfileForm,
    UpdateContactForm,
    AddAddressForm,
    UserAddress,
    User,
)


# Create your views here.
def sign_up(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công.")
            return redirect("sign_in")

    ctx = {
        "form": form,
    }

    return render(request, "account/sign_up.html", ctx)


def sign_in(request):
    form = SignInForm()
    next_url = request.GET.get("next")

    if request.method == "POST":
        remember = request.POST.get("remember", "off")
        form = SignInForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if remember == "on":
                    request.session.set_expiry(60 * 60 * 24 * 30 * 12)  # 1 year
                else:
                    request.session.set_expiry(60 * 60 * 24 * 7)  # 7 days

                login(request, user)
                redirect_url = next_url or resolve_url("home")
                messages.info(request, "Chào mừng trở lại.")
                return redirect(redirect_url)

    ctx = {
        "form": form,
    }

    return render(request, "account/sign_in.html", ctx)


@login_required
def sign_out(request):
    logout(request)
    return redirect("sign_in")


@login_required
def profile_manager(request):
    change_password_form = ChangePasswordForm(user=request.user)
    update_info_form = UpdateProfileForm(instance=request.user)
    update_contact_form = UpdateContactForm(instance=request.user)
    google_acc = request.user.socialaccount_set.filter(
        user=request.user,
        provider="google",
    )

    if google_acc.exists() and not request.user.has_usable_password():
        change_password_form = PasswordSetForm(user=request.user)

    add_address_form = AddAddressForm()
    user_address = UserAddress.objects.filter(user=request.user)

    ctx = {
        "change_password_form": change_password_form,
        "update_info_form": update_info_form,
        "update_contact_form": update_contact_form,
        "add_address_form": add_address_form,
        "user_address": user_address,
        "google_acc": google_acc,
    }

    return render(request, "account/profile_manager.html", ctx)


def deactivate_account(request):
    user = User.objects.filter(id=request.user.id)
    user.update(is_active=False)

    return redirect("sign_in")


def forgot_password(request):
    pass
