from rest_framework import serializers,status

from django.core.exceptions import ObjectDoesNotExist

from apps.account.models import *
from apps.store.models import *
from apps.delivery.models import *

class RecursiveField(serializers.BaseSerializer):
    def to_representation(self, value):
        depth = self.context.get('depth', 0)
        self.context['depth'] = depth+1
        ParentSerializer = self.parent.parent.__class__
        serializer = ParentSerializer(value, context=self.context, depth=self.context['depth'])

        return serializer.data

    def to_internal_value(self, data):
        ParentSerializer = self.parent.parent.__class__
        Model = ParentSerializer.Meta.model
        try:
            instance = Model.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "Objeto {0} does not exists".format(
                    Model().__class__.__name__
                )
            )
        return instance

class LocationSerializer(serializers.ModelSerializer):
    """This handles the location model

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
        fields = super(LocationSerializer,self).get_fields()
        if self.depth !=1:
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
            image = self.validated_data['image'],
            max_weight = self.validated_data['max_weight']
        )
        try:
            mean.save()
        except:
            raise serializers.ValidationError("You have already registered such means")
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
    """This handles the creation of a destination

    Args:
        serializers ([type]): [description]

    Returns:
        [type]: [description]
    """
    class Meta:
        model = Destination
        fields = ['location_from','location_to','price','means','id']
        read_only_fields = ['means','id']

    def save(self,means):
        """Handles saving a destination

        Args:
            means ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            destination = Destination(means = means,location_from= self.validated_data['location_from'],location_to = self.validated_data['location_to'],price=self.validated_data['price'])
            destination.save()
            return destination

        except Exception as e:
            print(e)
            raise serializers.ValidationError("You have already set such a destination!")

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