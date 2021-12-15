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
