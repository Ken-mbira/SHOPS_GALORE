from rest_framework import serializers

from apps.order.models import *
from apps.order.checkout import cart_to_order

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

class CheckoutSerializer(serializers.Serializer):
    """This defines the creation of an order from a cart

    Args:
        serializers ([type]): [description]

    Returns:
        [type]: [description]
    """
    id = serializers.CharField(max_length=9,min_length=8)
    location = serializers.CharField()

    def create_order(self,cart):
        try:
            location = Location.objects.get(pk = self.validated_data['location'])
            order = cart_to_order(cart.token,self.validated_data['id'],location)
            return order
        except Exception as e:
            print(e)
            raise serializers.ValidationError("There was a problem creating your order!")


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

class OrderItemSerializer(serializers.ModelSerializer):
    """This handles a single item of an order

    Args:
        serializers ([type]): [description]
    """
    requires_transit = serializers.BooleanField()
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    """This handles the order instance

    Args:
        serializers ([type]): [description]
    """
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['owner','made_on','delivery_means','staff_checked','delivered','id_password','location','items']