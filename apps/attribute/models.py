from django.db import models


# Create your models here.
class AbstractTimestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(AbstractTimestamp):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    description = models.TextField("Mô tả", max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Danh mục"
        verbose_name = "Danh mục"

    def __str__(self):
        return self.name


class Brand(AbstractTimestamp):
    name = models.CharField(max_length=100, verbose_name="Tên thương hiệu")
    description = models.TextField("Mô tả", max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Thương hiệu"
        verbose_name = "Thương hiệu"

    def __str__(self):
        return self.name


class Tag(AbstractTimestamp):
    name = models.CharField(max_length=100, verbose_name="Tên thẻ")
    description = models.TextField("Mô tả", max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Thẻ"
        verbose_name = "Thẻ"

    def __str__(self):
        return self.name.title()


class Color(AbstractTimestamp):
    name = models.CharField("Tên màu", max_length=50)
    hex_color_1 = models.CharField("Mã màu 1", max_length=7, default="#000000")
    hex_color_2 = models.CharField("Mã màu 2", max_length=7, null=True, blank=True)

    class Meta:
        # ordering = ["-created_at"]
        verbose_name_plural = "Màu sắc"
        verbose_name = "Màu sắc"

    def __str__(self):
        return self.name.title()


class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name="Tên kích cỡ")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Kích cỡ"
        verbose_name = "Kích cỡ"

    def __str__(self):
        return self.name.title()
