from apps.store.models import *

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

@receiver(post_save, sender=Product)
def create_stock_table(sender, instance, created, **kwargs):
    if created:
        if instance.sku is None:
            instance.sku = uuid.uuid4()
            instance.save()
        Stock.objects.create(product = instance,last_stock_check_date = datetime.now())