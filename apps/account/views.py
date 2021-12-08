from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.schemas import get_schema_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.account.serializers import *
from apps.account.models import *

class UserView(APIView):
    """This can create a user or be used to get all instances of users

    Args:
        generics ([type]): [description]
    """

    @swagger_auto_schema(request_body=RegisterSerializer,responses={200: "Your account was created successfully"})
    def post(self,request,format=None):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = "Your account was created successfully"
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)

class LoginView(APIView):
    """This handles a user login request

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    @swagger_auto_schema(request_body=LoginSerializer,responses={200: GetUserSerializer()})
    def post(self,request,format=None):
        data = {}
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validate_user()
            data['user'] = GetUserSerializer(user).data
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            responseStatus = status.HTTP_200_OK
            return Response(data,status = responseStatus)

        else:
            data = serializer.errors
            return Response(data,status = status.HTTP_400_BAD_REQUEST)