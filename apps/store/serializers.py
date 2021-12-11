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
        read_only_fields = ['logo','subscription_end_date','owner']

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