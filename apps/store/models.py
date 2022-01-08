from django.db import models
from datetime import datetime

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
    phone_contact = PhoneNumberField(region="KE")
    email_contact = models.EmailField()
    subscription_end_date = models.DateField(null=True)
    functional = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    @property
    def active(self):
        if (self.subscription_end_date is None) or datetime(self.subscription_end_date) < datetime.now() or (self.owner.is_active == False) or self.functional == False:
            return False
        return True

    @property
    def products(self):
        """This gets all the products within a shop
        """
        return Product.objects.filter(owner = self).count()

    def deactivate(self):
        self.functional = False
        self.save()



class Brand(models.Model):
    """This defines a brand and its logo

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length = 50)
    logo = models.ImageField(upload_to="brand_logos/",null=True)

class Category(MPTTModel):
    """Inventory category table

    Args:
        MPTTModel ([type]): [description]
    """
    name = models.CharField(
        max_length=100,
        verbose_name="category name",
        help_text="format: required, max_length=100"
    ) 

    is_active = models.BooleanField(
        default=True,
    )

    parent = TreeForeignKey("self",
    on_delete=models.PROTECT,
    related_name="children",
    null=True,
    unique=False,
    blank=True,
    verbose_name="parent of category",
    help_text="Format: not required"
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name="Product Category"
        verbose_name_plural="Product categories"

    def __str__(self):
        return self.name

class Type(models.Model):
    """This defines a general category of a product

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class Attribute(models.Model):
    """this defines the attributes associated with a product

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
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
    description = models.TextField(null=True)

    def __str__(self):
        return self.attribute.name + " - " + self.value

class Product(models.Model):
    """This defines the commodity and all the fields involved

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand,on_delete=models.PROTECT,related_name="product")
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name="product")
    type = models.ForeignKey(Type,on_delete=models.SET_NULL,related_name="product",null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Shop,on_delete=models.PROTECT,related_name="product")
    attribute_value = models.ManyToManyField(AttributeValue,related_name="product")
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=9,decimal_places=2,null=True,blank=True)
    discount_price = models.DecimalField(max_digits=9,decimal_places=2,null=True,blank=True)
    volume = models.IntegerField(null=True)
    sku = models.CharField(max_length=200,null=True,unique=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,related_name="children",
        null=True,
        unique=False,
        blank=True,
        verbose_name="parent of product",
        help_text="Format: not required"
    )

    class MPTTMeta:
        order_insertion_by = ['added_on']

    def __str__(self):
        return self.name

    @property
    def active(self):
        if self.owner.active and Media.objects.filter(product = self).count() > 4:
            return True
        return False

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
    comment = models.TextField(null=True)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return self.product.name + " rating"

class Stock(models.Model):
    """This defines the quantities of the products

    Args:
        models ([type]): [description]
    """
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name="stock")
    count = models.IntegerField()
    last_stock_check_date = models.DateField()

    def __str__(self):
        return self.product.name + " | stock"

class Media(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_images")
    image = models.ImageField(upload_to="product_image/")
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name + f" image - {self.pk}"