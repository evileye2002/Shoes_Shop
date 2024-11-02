import django_filters
from crispy_forms.helper import FormHelper
from django.db.models import Q

from apps.attribute.models import Color, Size, Brand
from .models import Shoe


class ShoeFilter(django_filters.FilterSet):
    minp = django_filters.NumberFilter(
        field_name="options__sizes__price",
        lookup_expr="gte",
    )
    maxp = django_filters.NumberFilter(
        field_name="options__sizes__price",
        lookup_expr="lte",
    )
    rating = django_filters.NumberFilter(
        field_name=("avg_review"),
        lookup_expr="gte",
    )
    brand = django_filters.ModelMultipleChoiceFilter(
        field_name="brand",
        queryset=Brand.objects.all(),
        conjoined=False,
    )
    color = django_filters.ModelMultipleChoiceFilter(
        field_name="options__color",
        queryset=Color.objects.all(),
        conjoined=False,
    )
    size = django_filters.ModelMultipleChoiceFilter(
        field_name="options__sizes__size",
        queryset=Size.objects.all(),
        conjoined=False,
    )

    class Meta:
        model = Shoe
        fields = ["minp", "maxp", "rating"]

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)

        self.form.helper = FormHelper()
        self.form.helper.form_method = "get"
