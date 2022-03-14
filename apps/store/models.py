from email.policy import default
from django.db import models
from datetime import datetime
import uuid

from phonenumber_field.modelfields import PhoneNumberField
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.account.models import User
from apps.delivery.models import *

class Shop(models.Model):
    """This defines involved in making a store
    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=50,unique=True)
    bio = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True,editable=False)
    owner = models.ForeignKey(User,on_delete=models.PROTECT,related_name="shops")
    logo = models.ImageField(upload_to="store_profiles/",null=True)
    pickup_location = models.ForeignKey(Location,on_delete=models.PROTECT,related_name="shop")
    phone_contact = PhoneNumberField()
    email_contact = models.EmailField()
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return Product.objects.filter(owner = self,active=True).count()

    def deactivate(self):
        self.active = False
        self.save()



class Brand(models.Model):
    """This defines a brand and its logo

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length = 50)
    logo = models.ImageField(upload_to="brand_logos/",null=True,blank=True)

class Category(MPTTModel):
    """Inventory category table

    Args:
        MPTTModel ([type]): [description]
    """
    name = models.CharField(max_length=100) 
    parent = TreeForeignKey("self",on_delete=models.PROTECT,related_name="children",null=True,blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name="Product Category"
        verbose_name_plural="Product Categories"

    def __str__(self):
        return self.name

class Type(models.Model):
    """This defines a general category of a product

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

class Attribute(models.Model):
    """this defines the attributes associated with a product

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    type = models.ManyToManyField(Type,related_name="attributes")

    def __str__(self):
        return self.name

class AttributeValue(models.Model):
    """This defines the values of an attribute

    Args:
        models ([type]): [description]
    """
    value = models.CharField(max_length=50)
    attribute = models.ForeignKey(Attribute,on_delete=models.PROTECT,related_name="attribute_values")
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.attribute.name + " - " + self.value

class Product(models.Model):
    """This defines the commodity and all the fields involved

    Args:
        models ([type]): [description]
    """
    sku = models.CharField(max_length=200,null=True,unique=True,blank=True)
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,related_name="products",null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name="products")
    type = models.ForeignKey(Type,on_delete=models.SET_NULL,related_name="products",null=True,blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Shop,on_delete=models.PROTECT,related_name="products")
    attribute_value = models.ManyToManyField(AttributeValue,related_name="products",blank=True)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=9,decimal_places=2,null=True,blank=True)
    discount_price = models.DecimalField(max_digits=9,decimal_places=2,null=True,blank=True)
    volume = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True,verbose_name="Volume in m3")
    weight = models.DecimalField(max_digits=5,decimal_places=2,verbose_name="Weight in kilograms",null=True,blank=True)
    parent = TreeForeignKey("self",on_delete=models.PROTECT,related_name="children",null=True,unique=False,blank=True,verbose_name="parent of product",)
    active = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ['added_on']

    def __str__(self):
        return self.name

    @property
    def featured_image(self):
        for image in Media.objects.filter(product = self):
            if image.is_default:
                return image
            continue
        return None

    @property
    def children(self):
        return Product.objects.filter(parent=self)

    @property
    def product_images(self):
        return Media.objects.filter(product = self)

class Review(models.Model):
    """This stores the customer opinions of the products

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="reviews",null=True,on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True,blank=True)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return self.product.name + " rating"

class Stock(models.Model):
    """This defines the quantities of the products

    Args:
        models ([type]): [description]
    """
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name="stock")
    count = models.IntegerField(default=0)
    last_stock_check_date = models.DateField()

    def __str__(self):
        return self.product.name + " | stock"

class Media(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_images")
    image = models.ImageField(upload_to="product_image/")
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name + f" image - {self.pk}"