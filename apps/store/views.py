from django.shortcuts import render

from rest_framework import permissions,generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.store.models import *
from apps.store.serializers import *
from apps.store.permissions import *

class StoreShopListView(generics.ListCreateAPIView):
    serializer_class = StoreShopSerializer
    permission_classes = [permissions.IsAuthenticated & IsShopOwner]

    def get_queryset(self):
        return Shop.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class StoreShopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = StoreShopSerializer
    permission_classes = [permissions.IsAuthenticated & IsShopOwner]

    def get_queryset(self):
        return Shop.objects.filter(owner = self.request.user)