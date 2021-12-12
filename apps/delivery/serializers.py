from rest_framework import serializers,status

from apps.account.models import *
from apps.store.models import *
from apps.delivery.models import *

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