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