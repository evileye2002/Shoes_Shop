from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .enums import UserGender


# Create your models here.
class UserCustom(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Số điện thoại",
    )
    gender = models.CharField(
        choices=UserGender.choices,
        max_length=6,
        blank=True,
        null=True,
        verbose_name="Giới tính",
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name="Ngày sinh",
    )
    bio = models.TextField(max_length=100, blank=True)
    avatar = models.ImageField(
        upload_to="images/avatars/",
        default="default/noimage.jpg",
    )

    def get_full_name(self) -> str:
        if self.last_name and self.first_name:
            return self.last_name + " " + self.first_name
        return self.username

    def mask_email(self):
        if not self.email:
            return ""

        user, domain = self.email.split("@")

        first_two = user[:2]
        last_two = user[-2:]

        num_asterisks = len(user) - 4

        masked_user = first_two + "*" * num_asterisks + last_two
        masked_email = f"{masked_user}@{domain}"

        return masked_email

    def mask_phone(self):
        if not self.phone:
            return ""

        if len(self.phone) != 10:
            return "Invalid phone number"

        first_three = self.phone[:2]
        last_three = self.phone[-3:]

        masked_phone = f"{first_three}*****{last_three}"

        return masked_phone


class UserAddress(models.Model):
    user = models.ForeignKey(
        UserCustom,
        on_delete=models.CASCADE,
        verbose_name="Người dùng",
    )

    address = models.CharField(max_length=255, verbose_name="Địa chỉ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Địa chỉ sử dụng"
        verbose_name = "Địa chỉ sử dụng"
