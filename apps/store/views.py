from django.shortcuts import render

from rest_framework import permissions,generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend

from apps.store.models import *
from apps.store.serializers import *
from apps.store.permissions import *
from apps.store.filters import *

class StoreShopListView(generics.ListCreateAPIView):
    serializer_class = StoreShopSerializer
    permission_classes = [permissions.IsAuthenticated & IsStoreOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active']

    def get_queryset(self):
        return Shop.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class StoreShopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = StoreShopSerializer
    permission_classes = [permissions.IsAuthenticated & IsStoreOwner]

    def get_queryset(self):
        return Shop.objects.filter(owner = self.request.user)

class StoreProductListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilters

    def get_queryset(self):
        return Product.objects.filter(owner__owner = self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST','PUT','PATCH']:
            return StoreCreateProductSerializer

        else:
            return StoreGetProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() and serializer.validate_the_owner(request.user):
                self.perform_create(serializer)
                return Response(serializer.data)

        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class StoreProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'sku'

    def get_queryset(self):
        return Product.objects.filter(owner__owner = self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST','PUT','PATCH']:
            return StoreCreateProductSerializer

        else:
            return StoreGetProductSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(),data=request.data)
        if serializer.is_valid() and serializer.validate_the_owner(request.user):
                self.perform_update(serializer)
                return Response(serializer.data)

        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class StoreTypeView(generics.ListAPIView):
    queryset = Type.objects.all()
    serializer_class = StoreTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class StoreBrandView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = StoreBrandSerializer
    permission_classes = [permissions.IsAuthenticated]

class StoreAttributeView(generics.ListAPIView):
    queryset = Attribute.objects.all()
    serializer_class = StoreAttributeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AttributeFilters

class StoreCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()

class CategoryView(APIView):
    """This handles the categories
    Args:
        APIView ([type]): [description]
    """
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request,format=None):
        """This lists all the categories out
        Args:
            request ([type]): [description]
            format ([type], optional): [description]. Defaults to None.
        """
        categories = Category.objects.filter(level=0)
        data = GetCategorySerializer(categories,many=True).data
        return Response(data,status.HTTP_200_OK)