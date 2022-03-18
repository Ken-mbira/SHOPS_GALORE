from rest_framework import serializers,status

from django.core.exceptions import ObjectDoesNotExist

from apps.account.models import *
from apps.store.models import *
from apps.delivery.models import *

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','name']

class DeliveryLocationSerializer(serializers.ModelSerializer):
    """This handles the categories when its a get request
    Args:
        serializers ([type]): [description]
    Returns:
        [type]: [description]
    """
    def __init__(self, *args, depth=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.depth = depth

    class Meta:
        model = Location
        fields = ['id','name']

    def get_fields(self):
        fields = super(DeliveryLocationSerializer,self).get_fields()
        if self.depth !=1:
            fields['children'] = DeliveryLocationSerializer(many=True,required=False)
        return fields

class DeliveryMeansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Means
        fields = '__all__'

class DeliveryRegisteredMeansImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredMeans
        fields = ['image']

    def update(self, instance, validated_data):
        instance.image = validated_data['image']
        instance.save()
        return instance

class DeliveryRegisteredMeansSerializer(serializers.ModelSerializer):
    delivery_means = DeliveryMeansSerializer(source='means',read_only=True)
    class Meta:
        model = RegisteredMeans
        fields = '__all__'
        read_only_fields = ['owner']

    def create(self, validated_data):
        try:
            means = RegisteredMeans.objects.create(**validated_data)
        except:
            raise serializers.ValidationError("You have already registered this means of travel!")

        return means


    def update(self, instance, validated_data):
        instance.max_weight = validated_data['max_weight']
        instance.max_volume = validated_data['max_volume']
        instance.active = validated_data['active']
        try:
            instance.save()
        except Exception as e:
            raise serializers.ValidationError("You have already registered this means of travel!")
        return instance

class DeliveryDestinationSerializer(serializers.ModelSerializer):
    registered_means = DeliveryRegisteredMeansSerializer(read_only=True,source="means")
    from_location = LocationSerializer(read_only=True,source="location_from")
    to_location = LocationSerializer(read_only=True,source="location_to")
    class Meta:
        model = Destination
        fields = '__all__'

    def validate_the_owner(self,user):
        if self.validated_data['means'].owner != user:
            raise serializers.ValidationError("You are not allowed to perform this action")
        return True

    def create(self, validated_data):
        return Destination.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.means = validated_data['means']
        instance.location_from = validated_data['location_from']
        instance.location_to = validated_data['location_to']
        instance.price = validated_data['price']
        instance.save()
        return instance