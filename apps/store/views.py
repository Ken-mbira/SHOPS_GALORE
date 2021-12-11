from re import A
from django.shortcuts import render

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.store.models import *
from apps.store.serializers import *
from apps.store.permissions import *

class RegisterShopView(APIView):
    """This creates the shop instance

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & ShopPermissions]

    @swagger_auto_schema(request_body=ShopSerializer(),responses={200:ShopSerializer})
    def post(self,request,format=None):
        serializer = ShopSerializer(data = request.data)

        if serializer.is_valid():
            data = ShopSerializer(serializer.save(request)).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

    @swagger_auto_schema(request_body=None,responses={200:ShopSerializer})
    def get(self,request,format = None):
        data = request.user.shops.all()
        data = ShopSerializer(data,many=True).data
        responseStatus = status.HTTP_200_OK

        return Response(data,responseStatus)

class UpdateShopView(APIView):
    """This handles requests to alter the shop instances

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsShopOwner]

    @swagger_auto_schema(request_body=ShopSerializer,responses={200:ShopSerializer})
    def put(self,request,id):
        serializer = ShopSerializer(data = request.data)

        try:
            instance = Shop.objects.get(pk = id)
        
        except:
            return Response("The shop was not found",status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            shop = serializer.update(Shop.objects.get(pk = id))
            data = ShopSerializer(shop).data
            responseStatus = status.HTTP_200_OK

        else:
            data = serializer.errors
            responseStatus = status.HTTP_404_NOT_FOUND

        return Response(data,responseStatus)

    @swagger_auto_schema(responses={200:"The shop was successfully deleted"})
    def delete(self,request,id):

        try:
            shop = Shop.objects.get(pk = id)
        except:
            return Response("The shops was not found",status.HTTP_404_NOT_FOUND)

        shop.deactivate()
        shop.save

        return Response("The shop was deleted successfully",status.HTTP_200_OK)
            