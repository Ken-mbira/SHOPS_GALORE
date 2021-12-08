from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.schemas import get_schema_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from apps.account.tokens import account_activation_token

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
            serializer.save(request)
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
    @swagger_auto_schema(request_body=LoginSerializer,responses={200: "User Token"})
    def post(self,request,format=None):
        data = {}
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validate_user()
            token, created = Token.objects.get_or_create(user=user)
            data = token.key
            responseStatus = status.HTTP_200_OK
            return Response(data,status = responseStatus)

        else:
            data = serializer.errors
            return Response(data,status = status.HTTP_400_BAD_REQUEST)

class UserInstanceView(APIView):
    """This return a user instance

    Args:
        APIView ([type]): [description]
    """
    @swagger_auto_schema(responses={200: GetUserSerializer()})
    def get(self,request,token):
        data = {}
        try:
            validated_token = Token.objects.get(key=token)
            data = GetUserSerializer(validated_token.user).data
            responseStatus = status.HTTP_200_OK
        except:
            data = "The token does not exist!"
            responseStatus = status.HTTP_404_NOT_FOUND

        return Response(data,status=responseStatus)


class ActivateAccount(APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        data = {}
        try:
            uid = uidb64
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            data['success'] = "Your account was successfully activated"

            return Response(data,status = status.HTTP_200_OK)
        else:
            data = 'The confirmation link was invalid, possibly because it has already been used.'
            return Response(data,status.HTTP_400_BAD_REQUEST)
