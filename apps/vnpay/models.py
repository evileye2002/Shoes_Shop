from django.db import models


# Create your models here.
class Payment(models.Model):
    order_id = models.CharField(max_length=250)
    order_type = models.CharField(max_length=20)
    amount = models.IntegerField()
    order_desc = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=2)
