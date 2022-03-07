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