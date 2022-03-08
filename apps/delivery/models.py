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
    """This entails the various ways of transportation available

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True,blank=True)
    logo = models.ImageField(upload_to="transport_means/",null=True,blank=True)

    def __str__(self):
        return self.name

class RegisteredMeans(models.Model):
    """This is a users registered means of transport

    Args:
        models ([type]): [description]
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="registered_means")
    means = models.ForeignKey(Means,on_delete=models.PROTECT,related_name="registered_means")
    image = models.ImageField(upload_to="registered_means/",null=True,blank=True)
    max_weight = models.DecimalField(max_digits=5,decimal_places=2)
    max_volume = models.DecimalField(max_digits=5,decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.owner.first_name + " - " + self.means.name

    class Meta:
        unique_together = ("owner","means")

class Destination(models.Model):
    """This shows the location covered by a means of transport along with the price

    Args:
        models ([type]): [description]
    """
    means = models.ForeignKey("delivery.RegisteredMeans",on_delete=models.CASCADE,related_name="destination")
    location_from = models.ForeignKey(Location,on_delete=models.PROTECT,related_name="from_location")
    location_to = models.ForeignKey(Location,on_delete=models.PROTECT,related_name="to_location")
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return str(self.means.pk) + " - " + self.location_from.name + " " + self.location_to.name 

    class Meta:
        unique_together = ("means","location_from","location_to")