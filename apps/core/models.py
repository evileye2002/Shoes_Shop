from django.db import models
from django.contrib.auth import get_user_model

from shortuuid.django_fields import ShortUUIDField
from django_ckeditor_5.fields import CKEditor5Field

from apps.base_account.models import UserAddress
from apps.attribute.models import Brand, Category, Tag, Size, Color
from .enums import PaymentMethods, OrderStatus, Rating

User = get_user_model()


# Create your models here.
class AbstractTimestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Shoe(AbstractTimestamp):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="shoes",
        verbose_name="Danh mục",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="shoes",
        verbose_name="Thương hiệu",
    )

    uuid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="SHOE")
    name = models.CharField(max_length=200, verbose_name="Tên giày")
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="shoes",
        verbose_name="Thẻ",
    )
    description = CKEditor5Field("Mô tả", config_name="default", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Giày"
        verbose_name = "Giày"

    def __str__(self):
        return self.name


class ShoeOption(AbstractTimestamp):
    uuid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="OPTION")

    shoe = models.ForeignKey(
        Shoe,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name="Giày",
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        related_name="options",
        verbose_name="Màu sắc",
    )

    class Meta:
        verbose_name_plural = "Chi tiết giày"
        verbose_name = "Chi tiết giày"

    def __str__(self) -> str:
        return f"{self.shoe.uuid} - Màu: {self.color}"


class ShoeOptionImage(models.Model):
    shoe_option = models.ForeignKey(
        ShoeOption,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(
        upload_to="images/shoes/",
        default="default/noimage.jpg",
        verbose_name="Ảnh",
    )

    class Meta:
        ordering = ["image"]
        verbose_name_plural = "Ảnh sản phẩm"
        verbose_name = "Ảnh sản phẩm"

    def __str__(self):
        return f"Image for {self.shoe_option.shoe.name} ({self.shoe_option.color})"


class ShoeOptionSize(models.Model):
    uuid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="SIZE")
    shoe_option = models.ForeignKey(
        ShoeOption,
        related_name="sizes",
        on_delete=models.CASCADE,
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Kích cỡ",
    )
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Giá cũ",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    quantity = models.PositiveIntegerField(verbose_name="Số lượng")

    class Meta:
        verbose_name_plural = "Kích cỡ sản phẩm"
        verbose_name = "Kích cỡ sản phẩm"

    def __str__(self):
        return f"{self.shoe_option.uuid} - Kích cỡ: {self.size}"


class Review(AbstractTimestamp):
    comment = models.TextField("Bình luận")
    rating = models.IntegerField(
        "Đánh giá",
        choices=Rating.choices,
        default=Rating.FIVE,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Người dùng",
    )
    shoe = models.ForeignKey(
        Shoe,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Giày",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Đánh giá"
        verbose_name = "Đánh giá"

    def __str__(self) -> str:
        return f"{self.user} - {self.shoe}"


class Order(AbstractTimestamp):
    uuid = ShortUUIDField(
        unique=True,
        length=10,
        max_length=20,
        alphabet="0123456789",
        verbose_name="Mã đơn hàng",
    )
    total_payment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Tổng tiền",
    )
    payment_method = models.CharField(
        max_length=6,
        choices=PaymentMethods.choices,
        verbose_name="Phương thức thanh toán",
    )
    status = models.CharField(
        max_length=9,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name="Trạng thái",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Người dùng",
    )
    shipping_address = models.ForeignKey(
        UserAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Địa chỉ giao hàng",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Đơn Hàng"
        verbose_name = "Đơn Hàng"

    def __str__(self) -> str:
        return self.uuid


class ShoppingCart(AbstractTimestamp):
    uuid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="CART")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Người dùng",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Giỏ hàng"
        verbose_name = "Giỏ hàng"

    def __str__(self) -> str:
        return self.user.username


class LineItem(AbstractTimestamp):
    uuid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ITEM")
    quantity = models.PositiveIntegerField(verbose_name="Số lượng")

    shoe_option_size = models.ForeignKey(
        ShoeOptionSize,
        on_delete=models.CASCADE,
        verbose_name="Kích cỡ",
    )
    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="items",
        verbose_name="Giỏ Hàng",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Đơn Hàng",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Mục hàng"
        verbose_name = "Mục hàng"

    def __str__(self) -> str:
        return self.uuid

    def get_total_price(self):
        return self.shoe_option_size.price * self.quantity

    def get_total_old_price(self):
        if self.shoe_option_size.old_price:
            return self.shoe_option_size.old_price * self.quantity
        else:
            return 0


class Payment(models.Model):
    order_id = models.CharField("Mã đơn hàng", max_length=20)
    amount = models.IntegerField("Giá trị đơn hàng")
    order_desc = models.CharField("Mô tả đơn hàng", max_length=100)
    bank_code = models.CharField("Mã ngân hàng", max_length=20, blank=True, null=True)
    pay_date = models.CharField("Ngày thanh toán", max_length=20)

    class Meta:
        ordering = ["-pay_date"]
        verbose_name_plural = "Lịch sử thanh toán"
        verbose_name = "Lịch sử thanh toán"
