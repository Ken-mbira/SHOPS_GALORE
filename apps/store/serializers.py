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

class StoreAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class StoreAttributeValueSerializer(serializers.ModelSerializer):
    attribute = StoreAttributeSerializer()
    class Meta:
        model = AttributeValue
        fields = '__all__'

class StoreCreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        attributes = validated_data.pop("attribute_value")
        product = Product.objects.create(**validated_data)
        for attribute in attributes:
            product.attribute_value.add(attribute)
        return product

class StoreGetProductSerializer(serializers.ModelSerializer):
    category = StoreCategorySerializer()
    brand = StoreBrandSerializer()
    type = StoreTypeSerializer()
    attribute_value = StoreAttributeValueSerializer()
    class Meta:
        model = Product
        fields = '__all__'
