from django.db import models

from apps.store.models import *
from apps.account.models import *
from apps.order.models import *
from apps.delivery.models import *

class Storage(models.Model):
    """These are the storage locations for goods on transit

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location,on_delete=models.PROTECT,related_name="storage_facility")


class DailyTransit(models.Model):
    """These entail the transport of order items from one storage to another

    Args:
        models ([type]): [description]
    """
    start_location = models.ForeignKey(Storage,on_delete=models.SET_NULL,null=True,related_name="transit_start_location")
    end_location = models.ForeignKey(Storage,on_delete=models.SET_NULL,null=True,related_name="transit_end_location")
    created_on = models.DateTimeField(auto_now_add=True)
    arrived_on = models.DateTimeField(null=True, blank=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return "transit -" + str(self.pk)

        