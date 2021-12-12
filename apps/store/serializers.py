from django.core.exceptions import ValidationError
from django.db.models import fields
from django.db.models.fields import IntegerField
from rest_framework import serializers

from apps.store.models import *

class ShopSerializer(serializers.ModelSerializer):
    """this handles the shop instances

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ['logo','subscription_end_date','owner','functional']

    def save(self,request):
        shop = Shop(name = self.validated_data['name'],bio = self.validated_data['bio'],owner = request.user,pickup_location = self.validated_data['pickup_location'],phone_contact = self.validated_data['phone_contact'],email_contact = self.validated_data['email_contact'])
        shop.save()
        return shop

    def update(self,instance):
        instance.name = self.validated_data['name']
        instance.bio = self.validated_data['bio']
        instance.pickup_location = self.validated_data['pickup_location']
        instance.phone_contact = self.validated_data['phone_contact']
        instance.email_contact = self.validated_data['email_contact']
        instance.save()
        return instance
        
class UpdateShopSerializer(serializers.Serializer):
    """This handles shop updating

    Args:
        serializers ([type]): [description]
    """
    shop = serializers.CharField(required=True)

    def delete(self):
        try:
            instance = Shop.objects.get(pk = int(self.validated_data['shop']))
        except:
            raise serializers.ValidationError("The object was not found")

        instance.deactivate()

    def validate_exists(self):
        try:
            Shop.objects.get(pk = int(self.validated_data['shop']))
            return True
        except:
            raise serializers.ValidationError("The object was not found")
    
class CreateProductSerializers(serializers.ModelSerializer):
    """This handles the creation of a new product

    Args:
        serializers ([type]): [description]
    """
    attributes = serializers.ListField()
    class Meta:
        model = Product
        fields = ['name','brand','category','type','description','price','attributes']

    def save(self,shop):
        product = Product(
            name = self.validated_data['name'],
            owner = shop,
            brand = self.validated_data['brand'],
            category = self.validated_data['category'],
            type = self.validated_data['type'],
            description = self.validated_data['description'],
            price = self.validated_data['price']
        )
        product.save()
        for value in self.validated_data['attributes']:
            attribute_value = AttributeValue.objects.get(pk = int(value))
            product.attribute_value.add(attribute_value)
            product.save()

        return product

    def update(self,instance):
        instance.name = self.validated_data['name']
        instance.brand = self.validated_data['brand']
        instance.category = self.validated_data['category']
        instance.type = self.validated_data['type']
        instance.description = self.validated_data['description']
        instance.price = self.validated_data['price']

        instance.save()
        return instance

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    """This handles the stocks for a single product

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Stock
        fields = '__all__'
        read_only_fields = ['product']

    def update(self,instance):
        instance.count = self.validated_data['count']
        instance.last_stock_check_date = self.validated_data['last_stock_check_date']
        instance.save()
        return instance.product

class GetShopSerializer(serializers.ModelSerializer):
    """This handles the response for getting all details about a shop

    Args:
        serializers ([type]): [description]
    """
    product = ProductSerializer(many=True)
    active = serializers.ReadOnlyField()
    class Meta:
        model = Shop
        fields = ['name','bio','created_on','owner','logo','pickup_location','phone_contact','email_contact','subscription_end_date','functional','active','product']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
        read_only_fields = ['product','is_default']

    def save(self,product):
        try:
            image = Media(product = product,image = self.validated_data['image'])
            image.save()
            return image
        except Exception as e:
            raise ValidationError("There was a problem updating your product image")

class GetProductSerializer(serializers.ModelSerializer):
    """This handles the response for a single product being viewed

    Args:
        serializers ([type]): [description]
    """
    product_images = ProductImagesSerializer(many=True)
    owner = ShopSerializer()
    stock = StockSerializer()
    brand = BrandSerializer()
    category = CategorySerializer()
    attribute_value = AttributeValueSerializer(many=True)
    class Meta:
        model = Product
        fields = [
            'name',
            'brand',
            'category',
            'type',
            'added_on',
            'owner',
            'attribute_value',
            'description',
            'price',
            'discount_price',
            'stock',
            'product_images'
        ]