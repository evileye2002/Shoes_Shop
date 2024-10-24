from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")

    class Meta:
        verbose_name_plural = "Danh mục"
        verbose_name = "Danh mục"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên thương hiệu")

    class Meta:
        verbose_name_plural = "Thương hiệu"
        verbose_name = "Thương hiệu"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên thẻ")

    class Meta:
        verbose_name_plural = "Thẻ"
        verbose_name = "Thẻ"

    def __str__(self):
        return self.name.title()


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name="Tên màu")
    hex_color = models.CharField("Mã màu (hex)", max_length=7)

    class Meta:
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
