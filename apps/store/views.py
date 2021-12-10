from django.shortcuts import render

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.store.models import *
from apps.store.serializers import *
from apps.store.permissions import *

class RegisterShop(APIView):
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