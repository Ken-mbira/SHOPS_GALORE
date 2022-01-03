from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from apps.account.tokens import account_activation_token
from apps.account.permissions import *

from apps.account.serializers import *
from apps.account.models import *

class UserView(APIView):
    """This can create a user or be used to get all instances of users

    Args:
        generics ([type]): [description]
    """
    permission_classes = [CheckRole]

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
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(responses={200: GetUserSerializer()})
    def get(self,request):
        data = GetUserSerializer(request.user).data
        responseStatus = status.HTTP_200_OK

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

class ProfileView(APIView):
    """This handles a users profile

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]

    @swagger_auto_schema(responses={200: ProfileSerializer()})
    def get(self,request,format=None):
        profile = Profile.objects.get(user = request.user)
        data = ProfileSerializer(profile).data
        return Response(data,status.HTTP_200_OK)

    @swagger_auto_schema(request_body= ProfileSerializer,responses={200: ProfileSerializer()})
    def put(self,request,format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.update(Profile.objects.get(user = request.user))
            data = ProfileSerializer(profile).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)

class ToggleNotificationView(APIView):
    """This toggles a user preference for receiving notifications via email

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]

    @swagger_auto_schema(request_body= NotificationPreferenceSerializer,responses={200: ProfileSerializer()})
    def put(self,request,format=None):
        serializer = NotificationPreferenceSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.change_preference(request)
            data = ProfileSerializer(profile).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)

class UpdateProfilePic(APIView):
    """This toggles a user preference for receiving notifications via email

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]

    @swagger_auto_schema(request_body= ProfilePicSerializer,responses={200: ProfileSerializer()})
    def put(self,request,format=None):
        serializer = ProfilePicSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.update_profile_pic(request)
            data = ProfileSerializer(profile).data
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)

class DeactivateOwnAccount(APIView):
    """This handles a users request to have their account deactivated

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]

    def put(self,request,format=None):
        request.user.deactivate_account()
        data = "Your account was deactivated"
        return Response(data,status=status.HTTP_200_OK)

class DeactivateOthersAccount(APIView):
    """This will handle the request to deactivate another users account

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsStaff]

    @swagger_auto_schema(request_body=AccountStatusSerializer,responses={200: "The users account was deactivated"})
    def post(self,request,format=None):
        serializer = AccountStatusSerializer(data=request.data)

        if serializer.is_valid() and serializer.validate_instance():
            serializer.deactivate_user()
            data = "The users account was deactivated"
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)


class ReinstateAccount(APIView):
    """This will handle the request to deactivate another users account

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & IsStaff]

    @swagger_auto_schema(request_body=AccountStatusSerializer,responses={200: "The user's account was reinstated"})
    def post(self,request,format=None):
        serializer = AccountStatusSerializer(data = request.data)

        if serializer.is_valid() and serializer.validate_instance():
            serializer.reinstate_user()
            data = "The user's account was reinstated"
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data,responseStatus)

class RegisterStaffView(APIView):
    """This entails the registration of a new staff member

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [permissions.IsAuthenticated & CheckRegisterNewStaff]

    @swagger_auto_schema(request_body=RegisterStaffSerializer,responses={200:"The staff member was created successfully"})
    def post(self,request,format=None):
        """This handles the creation of a staff member

        Args:
            request ([type]): [description]
            format ([type], optional): [description]. Defaults to None.
        """
        serializer = RegisterStaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            data = "The staff member was created successfully"
            responseStatus = status.HTTP_200_OK
        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,responseStatus)