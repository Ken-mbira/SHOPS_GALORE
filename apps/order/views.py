from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions,status

from drf_yasg.utils import swagger_auto_schema

from apps.order.serializers import *
from apps.order.models import *
from apps.order.permissions import *

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
        