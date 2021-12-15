from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions,status

from drf_yasg.utils import swagger_auto_schema

from apps.order.serializers import *
from apps.order.models import *
from apps.order.permissions import *
from apps.account.permissions import IsStaff

class CartView(APIView):
    """This handles the cart requests

    Args:
        APIView ([type]): [description]
    """

    permission_classes = [IsBuyerPermission & CheckCart]

    @swagger_auto_schema(responses={200:"token"})
    def post(self,request,format=None):
        try:
            if request.user.is_authenticated:
                cart = Cart.objects.create(owner = request.user)
            else:
                cart = Cart.objects.create()
            cart.save()
            data = cart.token
            responseStatus = status.HTTP_200_OK
        except Exception as e:
            print(e)
            data = "There was a problem creating your cart!"
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)

    def put(self,request,format=None):
        """This completes a cart instance

        Args:
            request ([type]): [description]
            format ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        try:
            cart = Cart.objects.get(token = (request.META.get("HTTP_CART_TOKEN")))
            cart.complete = True
            cart.save()
            data = "Your cart was successfully completed!"
            responseStatus = status.HTTP_200_OK
        except:
            data = "Your cart was not found"
            responseStatus = status.HTTP_404_NOT_FOUND

        return Response(data,responseStatus)

    def get(self,request,format=None):
        """This retrieves an open cart instance for an authenticated customer

        Args:
            request ([type]): [description]
            format ([type], optional): [description]. Defaults to None.
        """
        data = CartSerializer(Cart.objects.filter(owner = request.user,complete = False),many = True).data
        return Response(data,status.HTTP_200_OK)

class CartItemView(APIView):
    """This handles individual cart items

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [IsBuyerPermission & CheckCartExists]

    @swagger_auto_schema(request_body=CartItemSerializer,responses={200:CartSerializer()})
    def post(self,request,format=None):
        serializer = CartItemSerializer(data=request.data)
        cart = Cart.objects.get(token = request.META.get('HTTP_CART_TOKEN'))
        
        if serializer.is_valid():
            data = CartSerializer(serializer.save(cart)).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

    @swagger_auto_schema(request_body=CheckoutSerializer,responses={200:OrderSerializer()})
    def put(self,request,format=None):
        serializer = CheckoutSerializer(data=request.data)
        cart = Cart.objects.get(token = request.META.get('HTTP_CART_TOKEN'))

        if serializer.is_valid():
            data = OrderSerializer(serializer.create_order(cart)).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

class UpdateCartView(APIView):
    """This handles updating the contents of the cart

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [IsBuyerPermission & CheckCartExists]

    @swagger_auto_schema(responses={200:CartSerializer()})
    def put(self,request,id):
        try:
            item = CartItem.objects.get(pk = id)
        except:
            return Response("The item was not found",status.HTTP_404_NOT_FOUND)

        serializer = UpdateCartSerializer(data=request.data)
        if serializer.is_valid():
            data = CartSerializer(serializer.update_quantity(item)).data
            responseStatus = status.HTTP_200_OK

        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

    @swagger_auto_schema(responses={200:CartSerializer})
    def delete(self,request,id):
        try:
            item = CartItem.objects.get(pk = id)
        except:
            return Response("The item was not found",status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response("The cart item was removed!",status.HTTP_200_OK)

class OrderView(APIView):
    """This handles the viewing of order models

    Args:
        APIView ([type]): [description]
    """

    permission_classes = [IsBuyerPermission]

    @swagger_auto_schema(responses={200:OrderSerializer()})
    def get(self,request,format=None):
        """This gets all the pending orders for a user

        Args:
            request ([type]): [description]
            format ([type], optional): [description]. Defaults to None.
        """
        if request.META.get("HTTP_ORDER_TOKEN"):
            order = Order.objects.get(token = request.META.get("HTTP_ORDER_TOKEN"))
            data = OrderSerializer(order).data
            responseStatus = status.HTTP_200_OK
        else:
            data = "You have no active orders at the moment!"
            responseStatus = status.HTTP_404_NOT_FOUND
        
        return Response(data,responseStatus)