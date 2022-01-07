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

class ShopProductView(APIView):
    """This handles the products from a single shop

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsShopOwner]
    @swagger_auto_schema(responses={200:ShopSerializer()})
    def get(self,request,id):
        """This returns all the products in a shop

        Args:
            request ([type]): [description]
            format ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        data = ProductSerializer(Product.objects.filter(owner =  Shop.objects.get(pk = id)),many=True).data
        return Response(data,status.HTTP_200_OK)


class UpdateShopView(APIView):
    """This handles requests to alter the shop instances

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsShopOwner]

    @swagger_auto_schema(responses={200:ShopSerializer})
    def get(self,request,id):
        """This returns a single shop instance

        Args:
            request ([type]): [description]
            id ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            instance = Shop.objects.get(pk = id)
            data = ShopSerializer(instance).data
            return Response(data,status.HTTP_200_OK)
        
        except:
            return Response("The shop was not found",status.HTTP_404_NOT_FOUND)


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

    @swagger_auto_schema(responses={200: GetProductSerializer()})
    def get(self,request,id):
        product = Product.objects.get(pk = id)
        data = GetProductSerializer(product).data
        return Response(data,status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ProductImagesSerializer,responses={200: ProductImagesSerializer()})
    def post(self,request,id):
        """This creates a new image for the product

        Args:
            request ([type]): [description]
            id ([type]): [description]

        Returns:
            [type]: [description]
        """
        product = Product.objects.get(pk = id)
        serializer = ProductImagesSerializer(data = request.data)
        if serializer.is_valid():
            data = ProductImagesSerializer(serializer.save(product)).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)

    @swagger_auto_schema(request_body=CreateProductSerializers,responses={200: ProductSerializer()})
    def put(self,request,id):
        product = Product.objects.get(pk = id)
        serializer = CreateProductSerializers(data = request.data)
        if serializer.is_valid():
            data = ProductSerializer(serializer.update(product)).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)

class StockView(APIView):
    """This handles a products stock

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsProductOwner]

    @swagger_auto_schema(request_body=StockSerializer,responses={200: ProductSerializer()})
    def put(self,request,id):
        product = Product.objects.get(pk = id)
        serializer = StockSerializer(data = request.data)
        if serializer.is_valid():
            data = ProductSerializer(serializer.update(product.stock)).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

class UpdateDefaultImage(APIView):
    """This handles changing the default image for a product

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsProductOwner]

    @swagger_auto_schema(request_body=DefaultImageSerializer,responses={200: GetProductSerializer()})
    def post(self,request,id):
        product = Product.objects.get(pk = id)

        serializer = DefaultImageSerializer(data=request.data)
        if serializer.is_valid():
            data = GetProductSerializer(serializer.make_featured(product)).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)

class AttributeFilterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,id):
        try:
            type = Type.objects.get(pk = id)
        except :
            return Response("The type was not found",status.HTTP_404_NOT_FOUND)
        
        attributes = Attribute.objects.filter(type = type)

        data = AttributeSerializer(attributes,many=True).data
        return Response(data,status.HTTP_200_OK)

            
class ReviewView(APIView):
    """This handles creation of a new review

    Args:
        APIView ([type]): [description]
    """

    @swagger_auto_schema(request_body=ReviewSerializer,responses={200:ReviewSerializer()})
    def post(self,request,id):
        """This handles a brand new review

        Args:
            request ([type]): [description]
            format ([type], optional): [description]. Defaults to None.
        """
        try:
            product = Product.objects.get(pk = id)
        except:
            return Response("The product was not found",status.HTTP_404_NOT_FOUND)
        
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            data = ReviewSerializer(serializer.save(request,product)).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)

    def delete(self,request,id):
        """This handles deleting a posted review

        Args:
            request ([type]): [description]
            id ([type]): [description]
        """
        try:
            review = Review.objects.get(pk=id)
        except:
            return Response("The review was not found",status.HTTP_404_NOT_FOUND)

        review.delete()
        return Response("The review was deleted",status.HTTP_200_OK)
