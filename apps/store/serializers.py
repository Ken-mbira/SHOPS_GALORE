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