from rest_framework import serializers

from apps.order.models import *

class CartItemSerializer(serializers.ModelSerializer):
    """This handles the products in the cart

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['cart','quantity']

    def save(self,cart):
        try:
            item = CartItem(product = self.validated_data['product'],cart = cart)
            item.save()
            return item.cart
        except Exception as e:
            print(e)
            raise serializers.ValidationError("The product already exists in the cart")

class CartSerializer(serializers.ModelSerializer):
    """This handles the cart objects

    Args:
        serializers ([type]): [description]
    """
    cart_items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['owner','token','complete','created_at','cart_items']

class UpdateCartSerializer(serializers.Serializer):
    """This handles updating the quantities of items in carts

    Args:
        serializers ([type]): [description]
    """
    add = serializers.BooleanField(required=True)

    def update_quantity(self,instance):
        if self.validated_data['add']:
            instance.quantity += 1
            print(instance.quantity)
            instance.save()
        else:
            instance.quantity -= 1
            instance.save()

        if instance.quantity == 0:
            instance.delete()

        return instance.cart