from django.db import models

import uuid

from apps.store.models import *
from django.conf import settings

class Cart(models.Model):
    """This handles a users list of goods chosen for purchasing

    Args:
        models ([type]): [description]
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL,related_name="carts")
    token = models.CharField(max_length=30, null=True, blank=True, unique=True, default=uuid.uuid4())
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "cart- " + self.token

class CartItem(models.Model):
    """This is one instance of a product within a cart

    Args:
        models ([type]): [description]
    """
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name="cart_item")
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    added_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.cart.token + " - " + self.product.name