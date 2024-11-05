from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from .models import Order, OrderStatus


@receiver(post_save, sender=Order)
def update_item_quantities_on_delivery(sender, instance, **kwargs):
    if instance.status == OrderStatus.SHIPPING:
        for item in instance.items.all():
            item_quantity = item.quantity
            item.shoe_option_size.quantity = F("quantity") - item_quantity
            item.shoe_option_size.save(update_fields=["quantity"])
