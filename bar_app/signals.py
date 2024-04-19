import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem, Stock

logger = logging.getLogger(__name__)

@receiver(post_save, sender=OrderItem)
def update_stock(sender, instance, created, **kwargs):
    """
    Signal handler to update the stock count when a new OrderItem is created.
    """
    if created:
        reference = instance.reference
        bar = instance.order.bar
        stock = Stock.objects.get(reference=reference, bar=bar)
        stock.stock -= instance.count
        stock.save()

        if stock.stock < 2:
            logger.warning(f"Stock for reference '{reference.ref}' at bar '{bar.name}' is low: {stock.stock}")
