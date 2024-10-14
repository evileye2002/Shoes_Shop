from django.db import models


class UserGender(models.TextChoices):
    MALE = "male", "Nam"
    FEMALE = "female", "Nữ"
    OTHER = "other", "Khác"
