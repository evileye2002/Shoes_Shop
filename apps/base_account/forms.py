from django import forms
from django.urls import reverse
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm,
)
from django.contrib.auth import get_user_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, HTML

from .enums import UserGender
from .models import UserAddress
from .utils import submit_btn, delete_btn, indicator_elm

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        label="Tên",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Tên",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=150,
        label="Họ",
        widget=forms.TextInput(
            attrs={
                "autofocus": "",
                "placeholder": "Họ",
            }
        ),
    )
    username = forms.CharField(
        max_length=150,
        label="Tên đăng nhập",
        widget=forms.TextInput(
            attrs={
                "autocapitalize": "none",
                "autocomplete": "off",
                "placeholder": "Tên đăng nhập",
            }
        ),
    )
    email = forms.CharField(
        max_length=254,
        required=True,
        label="Địa chỉ email",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "off",
                "placeholder": "Địa chỉ email",
            }
        ),
    )
    password1 = forms.CharField(
        min_length=8,
        label="Mật khẩu",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Mật khẩu đăng nhập",
            }
        ),
    )
    password2 = forms.CharField(
        min_length=8,
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Xác nhận mật khẩu",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "last_name",
            "first_name",
            "email",
            "username",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""
        self.helper = FormHelper()
        # self.helper.form_method = "POST"
        # self.helper.form_action = "reverse('url_name')"

        self.helper.layout = Layout(
            Div(
                Field("last_name", wrapper_class="mb-0"),
                Field("first_name", wrapper_class="mb-0"),
                css_class="flex flex-col md:flex-row gap-x-3 gap-y-4",
            ),
            Field("email"),
            Field("username"),
            Field("password1"),
            Field("password2"),
            Submit(
                "submit",
                "Đăng ký tài khoản",
                css_class="w-full cursor-pointer text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800",
            ),
        )


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "autofocus": "",
                "autocapitalize": "none",
                "autocomplete": "username",
                "placeholder": "Tên đăng nhập hoặc email",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("username"),
            Field("password"),
            HTML(
                """
                <div class="flex items-start">
                    <div class="flex items-center h-5">
                        <input id="remember" aria-describedby="remember" name="remember" type="checkbox" class="w-4 h-4 border border-gray-300 rounded cursor-pointer bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800">
                    </div>
                    <div class="ml-3 text-sm">
                        <label for="remember" class="text-gray-500 cursor-pointer select-none dark:text-gray-300">Lưu phiên đăng nhập</label>
                    </div>
                </div>
                """
            ),
            Submit(
                "submit",
                "Đăng nhập",
                css_class="w-full cursor-pointer text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800",
            ),
        )


class UpdateProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(
        label="Giới tính",
        required=False,
        widget=forms.widgets.RadioSelect,
        choices=UserGender.choices,
    )
    birthday = forms.DateField(
        label="Ngày sinh",
        input_formats=["%d-%m-%Y"],
        required=False,
        widget=forms.DateInput(),
    )
    bio = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    class Meta:
        model = User
        fields = ["last_name", "first_name", "gender", "birthday", "bio"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = "w-full space-y-4"
        self.helper.attrs = {
            "oninput": "enableButton('update_info_submit');",
            "hx-target": "this",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #update_info_submit",
            "hx-post": reverse("htmx_update_info"),
        }

        self.helper.layout = Layout(
            Div(
                Field("last_name", wrapper_class="w-full !mb-0"),
                Field("first_name", wrapper_class="w-full !mb-0"),
                css_class="flex flex-col md:flex-row gap-x-3 gap-y-4",
            ),
            Div(
                Field(
                    "gender",
                    wrapper_class="w-full",
                    template="crispy_form/inline_radio_group.html",
                ),
                Field(
                    "birthday",
                    wrapper_class="w-full",
                    template="crispy_form/datepicker.html",
                ),
                css_class="flex flex-col md:flex-row gap-x-3 gap-y-4",
            ),
            Field("bio"),
            Div(
                HTML(indicator_elm()),
                HTML(submit_btn("update_info_submit")),
                css_class="flex items-center justify-end",
            ),
        )


class UpdateContactForm(forms.ModelForm):
    phone = forms.CharField(
        min_length=10,
        max_length=10,
        label="Số điện thoại",
        required=False,
    )

    class Meta:
        model = User
        fields = ["email", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = "p-4 !pt-0 md:p-5 space-y-4"
        self.helper.attrs = {
            "oninput": "enableButton('update_contact_submit');",
            "hx-target": "this",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #update_contact_submit",
            "hx-on::after-request": "closeModal('update-contact-modal');",
            "hx-post": reverse("htmx_update_contact"),
        }

        self.helper.layout = Layout(
            Field("email"),
            Field("phone"),
            Div(
                HTML(indicator_elm()),
                HTML(submit_btn("update_contact_submit")),
                css_class="flex items-center justify-end",
            ),
        )


class UpdateAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = ["address"]

    def __init__(self, *args, **kwargs):
        address_instance = kwargs.get("instance", None)
        super().__init__(*args, **kwargs)

        delete_url = ""
        self.helper = FormHelper()
        self.helper.form_class = "p-4 !pt-0 md:p-5 space-y-4"
        self.helper.form_show_labels = True
        self.helper.attrs = {
            "oninput": "enableButton('update_address_submit');",
            "hx-target": "this",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #update_address_submit",
        }

        if address_instance:
            delete_url = reverse(
                "htmx_delete_address",
                args=[address_instance.id],
            )
            self.helper.attrs["hx-post"] = reverse(
                "htmx_update_address",
                args=[address_instance.id],
            )

        self.helper.layout = Layout(
            Field("address", wrapper_class="!mb-0 w-full"),
            Div(
                HTML(indicator_elm("indicator_delete", True)),
                HTML(
                    delete_btn(
                        "delete_address_btn",
                        delete_url,
                        confirm_msg="Bạn có chắc chắn muốn xóa địa chỉ này?",
                        modal_close_id="update-address-modal",
                    )
                ),
                HTML(submit_btn("update_address_submit")),
                css_class="flex items-center justify-end gap-3",
            ),
        )


class AddAddressForm(UpdateAddressForm):
    address = forms.CharField(
        min_length=20,
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Thêm địa chỉ mới"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.form_class = "flex items-center gap-4"
        self.helper.form_show_labels = False
        self.helper.attrs = {
            "oninput": "enableButton('add_address_submit');",
            "hx-target": "#update-address-div",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #add_address_submit",
            "hx-post": reverse("htmx_add_address"),
        }

        self.helper.layout = Layout(
            Field("address", wrapper_class="!mb-0 w-full"),
            Div(
                HTML(indicator_elm()),
                HTML(submit_btn("add_address_submit", "Thêm")),
                css_class="flex items-center justify-end",
            ),
        )


class UpdateAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar"]


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password2"].help_text = ""

        self.helper = FormHelper()
        self.helper.form_class = "p-4 !pt-0 md:p-5 space-y-4"
        self.helper.attrs = {
            "oninput": "enableButton('change_password_submit');",
            "hx-target": "this",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #change_password_submit",
            "hx-post": reverse("htmx_change_password"),
        }

        self.helper.layout = Layout(
            Field("old_password"),
            Field("new_password1"),
            Field("new_password2"),
            Div(
                HTML(indicator_elm()),
                HTML(submit_btn("change_password_submit")),
                css_class="flex items-center justify-end",
            ),
        )


class PasswordSetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password2"].help_text = ""

        self.helper = FormHelper()
        self.helper.form_class = "p-4 !pt-0 md:p-5 space-y-4"
        self.helper.attrs = {
            "oninput": "enableButton('set_password_submit');",
            "hx-target": "this",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #set_password_submit",
            "hx-post": reverse("htmx_set_password"),
        }

        self.helper.layout = Layout(
            Field("new_password1"),
            Field("new_password2"),
            Div(
                HTML(indicator_elm()),
                HTML(submit_btn("set_password_submit")),
                css_class="flex items-center justify-end",
            ),
        )
