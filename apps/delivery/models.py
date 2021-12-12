from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

class Location(MPTTModel):
    """This designs how the location will be

    Args:
        MPTTModel ([type]): [description]
    """
    name = models.CharField(max_length=100)
    parent = TreeForeignKey("self",on_delete=models.PROTECT,related_name="children",null=True,blank=True)

    def __str__(self):
        return self.name
