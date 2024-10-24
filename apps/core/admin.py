from django.contrib import admin
from django.utils.html import format_html


from .models import (
    Category,
    Brand,
    Size,
    Color,
    Tag,
    Shoe,
    ShoeOption,
    ShoeOptionImage,
    Order,
    ShoppingCart,
    LineItem,
    Review,
)


# Register your models here.
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "brand",
        "uuid",
        "image_tag",
    )
    search_fields = ("name", "category__name", "brand__name")
    list_filter = ("category__name", "brand__name")
    readonly_fields = ("uuid",)
    inlines = [ReviewInline]

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

    image_tag.short_description = "Ảnh"


class ShoeOptionImageInline(admin.TabularInline):
    model = ShoeOptionImage
    extra = 1
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


@admin.register(ShoeOption)
class ShoeOptionAdmin(admin.ModelAdmin):
    list_display = ("shoe", "size", "color", "quantity", "price", "discount_tag")
    search_fields = ("shoe__name", "size", "color")
    list_filter = ("shoe__name", "size", "color")
    readonly_fields = ("uuid",)
    inlines = [ShoeOptionImageInline]

    def discount_tag(self, obj):
        if obj.old_price and obj.old_price > 0:
            discount = round(
                (obj.old_price - obj.price) / obj.old_price * 100,
                0,
            )
            return f"{discount}%"
        return "0%"

    discount_tag.short_description = "Giảm giá"


class LineItemInline(admin.TabularInline):
    readonly_fields = ("uuid",)
    model = LineItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
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
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("uuid", "user")
    search_fields = ("uuid", "user__username")
    readonly_fields = ("uuid",)
    inlines = [LineItemInline]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Tag)
