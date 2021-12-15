from rest_framework import serializers

from apps.order.models import *

class CartSerializer(serializers.ModelSerializer):
    """This handles the cart objects

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Cart
        fields = '__all__'