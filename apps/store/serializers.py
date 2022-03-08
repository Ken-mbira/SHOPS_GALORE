from turtle import update
from unicodedata import category
from rest_framework import serializers

from apps.store.models import *

class StoreShopSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ['owner']

    def create(self, validated_data):
        return Shop.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.name = validated_data['name']
        instance.bio = validated_data['bio']
        instance.logo = validated_data['logo']
        # instance.pickup_location = validated_data['pickup_location']
        instance.phone_contact = validated_data['phone_contact']
        instance.email_contact = validated_data['email_contact']
        instance.active = validated_data['active']
        instance.save()
        return instance

class StoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class StoreBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class StoreTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class StoreAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        exclude = ["attribute"]

class StoreAttributeSerializer(serializers.ModelSerializer):
    attribute_values = StoreAttributeValueSerializer(many=True)
    class Meta:
        model = Attribute
        fields = '__all__'

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute = ProductAttributeSerializer()
    class Meta:
        model = AttributeValue
        fields = '__all__'

class StoreCreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_the_owner(self,user):
        if self.validated_data['owner'].owner != user:
            raise serializers.ValidationError("You are not allowed to perform this action")
        return True

    def create(self, validated_data):
        attributes = validated_data.pop("attribute_value")
        product = Product.objects.create(**validated_data)
        for attribute in attributes:
            product.attribute_value.add(attribute)
        return product

    def update(self, instance, validated_data):
        attributes = validated_data.pop("attribute_value")
        instance.name = validated_data['name']
        instance.category = validated_data['category']
        instance.type = validated_data['type']
        instance.owner = validated_data['owner']
        instance.description = validated_data['description']
        instance.price = validated_data['price']
        instance.discount_price = validated_data['discount_price']
        instance.volume = validated_data['volume']
        instance.weight = validated_data['weight']
        instance.active = validated_data['active']
        for attribute in attributes:
            instance.attribute_value.add(attribute)

        instance.save()
        return instance

class StoreGetProductSerializer(serializers.ModelSerializer):
    category = StoreCategorySerializer()
    brand = StoreBrandSerializer()
    type = StoreTypeSerializer()
    attribute_value = ProductAttributeValueSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'