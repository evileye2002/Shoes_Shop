from django.db import models


class PaymentMethods(models.TextChoices):
    ONLINE_PAYMENT = "online", "Thanh toán trực tuyến"
    CASH_ON_DELIVERY = "cash", "Thanh toán khi nhận hàng"


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Đang chờ"
    PREPARING = "preparing", "Đang chuẩn bị"
    SHIPPED = "shipped", "Đã vận chuyển"
    DELIVERED = "deliverd", "Đã nhận"
    CANNCELED = "cannceled", "Đã huỷ đơn"


class Rating(models.IntegerChoices):
    ONE = 1, "1 sao"
    TWO = 2, "2 sao"
    THREE = 3, "3 sao"
    FOUR = 4, "4 sao"
    FIVE = 5, "5 sao"
