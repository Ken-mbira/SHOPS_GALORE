from django.shortcuts import render
from rest_framework import response

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions,generics
from drf_yasg.utils import swagger_auto_schema

from apps.account.models import *
from apps.store.models import *
from apps.delivery.models import *
from apps.delivery.serializers import *
from apps.delivery.permissions import *

class DeliveryLocationView(APIView):
    """This handles the categories
    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsDeliveryPerson]

    def get(self,request,format=None):
        """This lists all the categories out
        Args:
            request ([type]): [description]
            format ([type], optional): [description]. Defaults to None.
        """
        locations = Location.objects.filter(level=0)
        data = DeliveryLocationSerializer(locations,many=True).data
        return Response(data,status.HTTP_200_OK)

class DeliveryMeansView(generics.ListAPIView):
    queryset = Means.objects.all()
    serializer_class = DeliveryMeansSerializer
    permission_classes = [permissions.IsAuthenticated & IsDeliveryPerson]

class DeliveryRegisteredMeansListView(generics.ListCreateAPIView):
    serializer_class = DeliveryRegisteredMeansSerializer
    permission_classes = [permissions.IsAuthenticated & IsDeliveryPerson]

    def get_queryset(self):
        return RegisteredMeans.objects.filter(owner = self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class DeliveryRegisteredMeansDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeliveryRegisteredMeansSerializer
    pemission_classes = [permissions.IsAuthenticated & IsDeliveryPerson]

    def get_queryset(self):
        return RegisteredMeans.objects.filter(owner = self.request.user)

