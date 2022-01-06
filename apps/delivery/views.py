from django.shortcuts import render
from rest_framework import response

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions
from drf_yasg.utils import swagger_auto_schema

from apps.account.models import *
from apps.store.models import *
from apps.delivery.models import *
from apps.delivery.serializers import *
from apps.delivery.permissions import *

class LocationView(APIView):
    """This handles the getting of all the locations

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200:LocationSerializer()})
    def get(self,request,format=None):
        locations = Location.objects.filter(level=0)
        data = LocationSerializer(locations,many=True).data
        return Response(data,status.HTTP_200_OK)

class DeliveryMeansView(APIView):
    """This handles requests for a users means

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsDeliveryGuy]

    @swagger_auto_schema(request_body=RegisterMeansSerializer,responses={200: RegisterMeansSerializer()})
    def post(self,request,format=None):
        serializer = RegisterMeansSerializer(data=request.data)
        if serializer.is_valid():
            data = RegisterMeansSerializer(serializer.save(request)).data
            responseStatus = status.HTTP_200_OK

        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

    @swagger_auto_schema(responses={200: RegisterMeansSerializer()})
    def get(self,request,format=None):
        means = DeliveryMeans.objects.filter(owner = request.user)
        data = RegisterMeansSerializer(means,many=True).data
        
        return Response(data,status.HTTP_200_OK)

class UpdateMeans(APIView):
    """This handles updating a single means

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsMeansOwner]

    @swagger_auto_schema(request_body=DestinationSerializer,responses={200:DestinationSerializer()})
    def post(self,request,id):
        means = DeliveryMeans.objects.get(pk = id)
        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            data = DestinationSerializer(serializer.save(means)).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

    @swagger_auto_schema(request_body=DeliveryMeansImage,responses={200:DeliveryMeansImage()})
    def put(self,request,id):
        means = DeliveryMeans.objects.get(pk = id)
        serializer = DeliveryMeansImage(data=request.data)
        if serializer.is_valid():
            serializer.save(means)
            data = "The image was successfully updated"
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)

    @swagger_auto_schema(responses={200:"The image was successfully deleted"})
    def delete(self,request,id):
        means = DeliveryMeans.objects.get(pk=id)
        means.delete()
        data = "The image was successfully deleted"
        return Response(data,status.HTTP_200_OK)

class DestinationView(APIView):
    """This handles a single destination

    Args:
        APIView ([type]): [description]
    """
    @swagger_auto_schema(request_body=DestinationPriceSerializer,responses={200:"The destination was successfully updated"})
    def put(self,request,id):
        destination = Destination.objects.get(pk = id)

        serializer = DestinationPriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(destination)
            data = "The destination was successfully updated"
            responseStatus = status.HTTP_200_OK

        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

    @swagger_auto_schema(responses={200:"The destination was deleted"})
    def delete(self,request,id):
        destination = Destination.objects.get(pk = id)
        destination.delete()
        data = "The destination was deleted"
        return Response(data,status.HTTP_200_OK)