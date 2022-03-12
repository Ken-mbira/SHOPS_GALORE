from django.http import response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.authtoken.models import Token
from apps.account.tokens import account_activation_token

from apps.account.permissions import *
from apps.account.serializers import *
from apps.account.models import *

class UserView(generics.CreateAPIView):
    """This can create a user or be used to get all instances of users

    Args:
        generics ([type]): [description]
    """
    serializer_class = RegisterSerializer
    permission_classes = [CheckRole]

class AccountUserView(generics.RetrieveAPIView):
    """This return a user instance

    Args:
        APIView ([type]): [description]
    """
    serializer_class = AccountUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class AccountProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = AccountProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class GoogleSingUpView(APIView):

    @swagger_auto_schema(request_body=SocialSignUpSerializer(),responses={200:"Refresh and Access Tokens"})
    def post(self,request):
        serializer = SocialSignUpSerializer(data = request.data)

        if serializer.is_valid() and serializer.validate_user_role():
            user = serializer.validate_google_auth_token()
            data = user.tokens()
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

class FacebookSingUpView(APIView):

    @swagger_auto_schema(request_body=SocialSignUpSerializer(),responses={200:"Refresh and Access Tokens"})
    def post(self,request):
        serializer = SocialSignUpSerializer(data = request.data)

        if serializer.is_valid() and serializer.validate_user_role():
            user = serializer.validate_facebook_auth_token()
            data = user.tokens()
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

class GoogleLoginView(APIView):

    def post(self,request):
        serializer = SocialLoginSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.google_social_login()
            data = user.tokens()
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

class FacebookLoginView(APIView):

    def post(self,request):
        serializer = SocialLoginSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.facebook_social_login()
            data = user.tokens()
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)