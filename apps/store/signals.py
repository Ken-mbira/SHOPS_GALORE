from apps.store.models import *

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

@receiver(post_save, sender=Product)
def create_stock_table(sender, instance, created, **kwargs):
    if created:
        Stock.objects.create(product = instance,count=0,last_stock_check_date = datetime.now())