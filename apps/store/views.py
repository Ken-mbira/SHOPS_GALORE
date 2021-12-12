from re import A
from django.shortcuts import render

from rest_framework import permissions
from rest_framework import response
from rest_framework.test import APITestCase
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

    @swagger_auto_schema(responses={200:"The shop was successfully deactivated"})
    def delete(self,request,id):

        try:
            shop = Shop.objects.get(pk = id)
        except:
            return Response("The shops was not found",status.HTTP_404_NOT_FOUND)

        shop.deactivate()
        shop.save

        return Response("The shop was successfully deactivated",status.HTTP_200_OK)

    
class DeleteShopView(APIView):
    """This adds a full delete option to the shop

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsShopOwner]

    def delete(self,request,id):
        try:
            shop = Shop.objects.get(pk = id)
        except:
            return Response("The shops was not found",status.HTTP_404_NOT_FOUND)

        shop.delete()

        return Response("The shop was deleted successfully",status.HTTP_200_OK)

class CreateProductView(APIView):
    """This creates a new product

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsShopOwner & ShopPermissions]

    @swagger_auto_schema(request_body=CreateProductSerializers,responses={200:ProductSerializer()})
    def post(self,request,id):
        serializer = CreateProductSerializers(data = request.data)
        if serializer.is_valid():
            data = ProductSerializer(serializer.save(shop = Shop.objects.get(pk = id))).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

    @swagger_auto_schema(responses={200:GetShopSerializer()})
    def get(self,request,id):
        try:
            shop = Shop.objects.get(pk = id)
        except:
            return Response("The shop was not found")

        data = GetShopSerializer(shop).data
        return Response(data,status.HTTP_200_OK)

class BrandView(APIView):
    """This handles the view of brands

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: BrandSerializer()})
    def get(self,request,format=None):
        brands = Brand.objects.all()
        data = BrandSerializer(brands,many=True).data
        return Response(data,status.HTTP_200_OK)

class TypeView(APIView):
    """This handles the view of types

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: TypeSerializer()})
    def get(self,request,format=None):
        brands = Type.objects.all()
        data = TypeSerializer(brands,many=True).data
        return Response(data,status.HTTP_200_OK)
        

class SingleProductView(APIView):
    """This handles the request for a specific product

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsProductOwner]

    def get(self,request,id):
        product = Product.objects.get(pk = id)
        data = GetProductSerializer(product).data
        return Response(data,status.HTTP_200_OK)