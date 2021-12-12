from django.db import models
from django.conf import settings

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

class Means(models.Model):
    """This entails the various ways of transportation

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to="transport_means/",null=True)
    rank = models.IntegerField()

    def __str__(self):
        return self.name

class DeliveryMeans(models.Model):
    """This is a users registered means of transport

    Args:
        models ([type]): [description]
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="registered_means")
    means = models.ForeignKey(Means,on_delete=models.PROTECT,related_name="registered_means")
    image = models.ImageField(upload_to="registered_means/",null=True)

    def __str__(self):
        return self.owner.first_name + " - " + self.means.name

class Destination(models.Model):
    """This shows the location covered by a means of transport along with the price

    Args:
        models ([type]): [description]
    """
    means = models.ForeignKey(DeliveryMeans,on_delete=models.CASCADE,related_name="destination")
    location = models.ForeignKey(Location,on_delete=models.PROTECT,related_name="destination")
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        self.means + " - " + self.location.name