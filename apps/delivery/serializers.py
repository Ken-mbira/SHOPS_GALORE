from rest_framework import serializers,status

from apps.account.models import *
from apps.store.models import *
from apps.delivery.models import *

class RecursiveField(serializers.Serializer):

    def to_native(self,value):
        return LocationSerializer(value,context = {"parent":self.parent.object, "parent_serializer":self.parent})

class LocationSerializer(serializers.ModelSerializer):
    """This handles the location model

    Args:
        serializers ([type]): [description]

    Returns:
        [type]: [description]
    """
    class Meta:
        model = Location
        fields = ['id','name']

    def get_fields(self):
        fields = super(LocationSerializer,self).get_fields()
        fields['children'] = LocationSerializer(many=True,required=False)
        return fields

class RegisterMeansSerializer(serializers.ModelSerializer):
    """This handles the means

    Args:
        serializers ([type]): [description]

    Returns:
        [type]: [description]
    """
    class Meta:
        model = DeliveryMeans
        fields = '__all__'
        read_only_fields = ['owner']

    def save(self,request):
        mean = DeliveryMeans(
            owner = request.user,
            means = self.validated_data['means'],
            image = self.validated_data['image']
        )

        mean.save()
        return mean

class DeliveryMeansImage(serializers.Serializer):
    """This adds a way to update the image for a means

    Args:
        serializers ([type]): [description]
    """
    image = serializers.ImageField(required=True)

    def save(self,means):
        means.image = self.validated_data['image']
        means.save()

class DestinationSerializer(serializers.ModelSerializer):
    """This will handle a destination for a specific location

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Destination
        fields = '__all__'
        read_only_fields = ['means']

    def save(self,means):
        destination = Destination(
            means = means,
            location = self.validated_data['location'],
            price = self.validated_data['price']
        )
        destination.save()
        return destination

class DestinationPriceSerializer(serializers.Serializer):
    """This handles updating a destination's price

    Args:
        serializers ([type]): [description]
    """
    price = serializers.DecimalField(max_digits=10,decimal_places=2)

    def save(self,destination):
        destination.price = self.validated_data['price']
        destination.save()
        return destination