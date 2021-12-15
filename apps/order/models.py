from django.db import models
from django.contrib.auth.hashers import make_password

import uuid

from apps.store.models import *
from apps.delivery.models import *
from django.conf import settings

class Cart(models.Model):
    """This handles a users list of goods chosen for purchasing

    Args:
        models ([type]): [description]
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="carts")
    token = models.CharField(max_length=30, null=True, blank=True, unique=True)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "cart- " + self.token

    def save(self,**kwargs):
        if self.token is None:
            self.token  = uuid.uuid4()
        super().save()

class CartItem(models.Model):
    """This is one instance of a product within a cart

    Args:
        models ([type]): [description]
    """
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,related_name="cart_item")
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    added_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.cart.token + " - " + self.product.name

    class Meta:
        unique_together = ("product","cart")

class ShopDailyOrders(models.Model):
    """This will hold all the orders from a shop on a particular day

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    shop = models.ForeignKey(Shop,on_delete=models.SET_NULL,null=True,related_name="daily_orders")
    pickup_means = models.ForeignKey(DeliveryMeans,on_delete=models.SET_NULL,null=True,related_name="daily_orders")
    date = models.DateField(auto_now_add=True,editable=False)

    def __str__(self):
        return self.shop.name + " - " + str(self.date)

class Order(models.Model):
    """This is a summary of a completed purchase

    Args:
        models ([type]): [description]
    """
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    made_on = models.DateTimeField(auto_now_add=True,editable=False)
    delivery_means = models.ForeignKey(DeliveryMeans,on_delete=models.SET_NULL,null=True)
    staff_checked = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    id_password = models.CharField(max_length=256)
    location = models.ForeignKey(Location,on_delete=models.PROTECT,related_name="orders")
    token = models.CharField(max_length=20,null=True,blank=True,unique=True)

    def save(self,**kwargs):
        some_salt = 'some_salt' 
        self.id_password = make_password(self.id_password,some_salt)

        if self.token is None:
            self.token = uuid.uuid4()
        super().save(**kwargs)

    def __str__(self):
        return "order - " + str(self.pk) + " to " +self.location.name

class OrderItem(models.Model):
    """This contains a single item within an order instance

    Args:
        models ([type]): [description]
    """
    order = models.ForeignKey(Order,on_delete=models.PROTECT,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name="order_items")
    quantity = models.IntegerField()
    current_price = models.DecimalField(max_digits=9,decimal_places=2)
    seller_checked = models.BooleanField(default=False)
    rider_checked = models.BooleanField(default=False)
    staff_one_checked = models.BooleanField(default=False)
    staff_two_checked = models.BooleanField(null=True)
    daily_order = models.ForeignKey(ShopDailyOrders,on_delete=models.PROTECT,related_name="item")

    @property
    def requires_transit(self):
        try:
            if self.order.location.parent == self.product.owner.pickup_location.parent:
                return False
            return True
        except:
            return None

    @property
    def dispatched(self):
        if self.rider_checked and self.seller_checked:
            return True
        return False