from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin
from .models import (
    Shoe,
    ShoeOption,
    ShoeOptionImage,
    ShoeOptionSize,
    Order,
    ShoppingCart,
    LineItem,
    Review,
)


# Register your models here.
class ShoeOptionSizeInline(admin.TabularInline):
    model = ShoeOptionSize
    extra = 1
    min_num = 1
    readonly_fields = ("uuid",)


class ShoeOptionImageInline(admin.TabularInline):
    model = ShoeOptionImage
    extra = 1
    min_num = 1
    readonly_fields = ["image_tag"]

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                f"""
                <div style="height: 70px; width: 70px;display: flex;align-items: center;justify-items: center;">
                    <img src="{obj.image.url}" style="width: 100%;"/>
                </div>
                """
            )
        return "-"

    image_tag.short_description = "Ảnh xem trước"


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


class LineItemInline(admin.TabularInline):
    model = LineItem
    readonly_fields = ("uuid",)
    extra = 1


@admin.register(Shoe)
class ShoeAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "category",
        "brand",
        "uuid",
    )
    search_fields = ("name", "category__name", "brand__name")
    list_filter = ("category__name", "brand__name")
    readonly_fields = ("uuid",)
    inlines = [ReviewInline]


@admin.register(ShoeOption)
class ShoeOptionAdmin(ImportExportModelAdmin):
    list_display = (
        "shoe",
        "color",
        "uuid",
    )
    search_fields = ("color", "uuid")
    list_filter = ("shoe__name", "color")
    readonly_fields = ("uuid",)
    inlines = [ShoeOptionImageInline, ShoeOptionSizeInline]


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    list_display = (
        "uuid",
        "user",
        "total_payment",
        "payment_method",
        "status",
        "shipping_address",
    )
    search_fields = (
        "uuid",
        "user__username",
    )
    list_filter = ("status", "payment_method")
    readonly_fields = ("uuid",)
    inlines = [LineItemInline]


@admin.register(ShoppingCart)
class ShoppingCartAdmin(ImportExportModelAdmin):
    list_display = ("uuid", "user")
    search_fields = ("uuid", "user__username")
    readonly_fields = ("uuid",)
    inlines = [LineItemInline]


admin.site.register(ShoeOptionSize, ImportExportModelAdmin)
admin.site.register(ShoeOptionImage, ImportExportModelAdmin)
admin.site.register(Review, ImportExportModelAdmin)
admin.site.register(LineItem, ImportExportModelAdmin)
