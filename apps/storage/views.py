from django.shortcuts import render

from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.storage.models import *
from apps.storage.serializers import *
from apps.account.permissions import *

# Create your views here.

class StorageView(APIView):
    """This handles storage locations

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsStaff]

    @swagger_auto_schema(request_body=StorageSerializer,responses={200:StorageSerializer()})
    def post(self,request,format=None):
        """This creates a new storage location

        Args:
            request ([type]): [description]
            format ([type], optional): [description]. Defaults to None.
        """
        serializer = StorageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create()
            data = "The storage location was created successfully"
            responseStatus = status.HTTP_200_OK

        else:
            data = "There was a problem creating the storage location"
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

class UpdateStorageView(APIView):
    """This handles updating the storage location details

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsStaff]

    @swagger_auto_schema(request_body = UpdateStorageSerializer,responses={200:StorageSerializer()})
    def put(self,request,id):
        """This updates the name of the storage location

        Args:
            request ([type]): [description]
            id ([type]): [description]
        """
        serializer = UpdateStorageSerializer(data=request.data)
        try:
            storage = Storage.objects.get(pk = id)

        except:
            return Response("The storage location was not found",status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            data = StorageSerializer(serializer.update(storage)).data
            responseStatus = status.HTTP_200_OK

        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)

    @swagger_auto_schema(responses={200:"The storage location was successfully deleted"})
    def delete(self,request,id):
        try:
            storage = Storage.objects.get(pk = id)

        except:
            return Response("The storage location was not found",status.HTTP_404_NOT_FOUND)

        storage.delete()
        return Response("The storage location was successfully deleted",status.HTTP_200_OK)

    @swagger_auto_schema(responses={200:StorageSerializer()})
    def get(self,request,id):
        try:
            storage = Storage.objects.get(pk = id)

        except:
            return Response("The storage location was not found",status.HTTP_404_NOT_FOUND)

        data = StorageSerializer(storage).data
        return Response(data,status.HTTP_200_OK)