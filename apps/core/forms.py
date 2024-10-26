from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, HTML

from .models import Order
from apps.base_account.models import UserAddress


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["payment_method", "shipping_address"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["shipping_address"].queryset = UserAddress.objects.filter(
                user=user
            )

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                """ 
                <p class="mb-4 text-xl font-semibold text-gray-900 dark:text-white">Thông tin giao hàng</p>
            """
            ),
            Field("payment_method", wrapper_class="!mb-0"),
            Field("shipping_address", wrapper_class="!mb-0"),
            HTML(
                """ 
                <button 
                    type="submit" 
                    name="action" 
                    value="checkout" 
                    class="w-full cursor-pointer text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">
                    Đặt hàng
                </button>
            """
            ),
        )
