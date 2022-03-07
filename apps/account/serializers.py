from multiprocessing import AuthenticationError
from rest_framework import serializers
from phonenumber_field.modelfields import PhoneNumberField
from decouple import config

from apps.account.models import *
from apps.storage.models import *
from apps.account import google
from apps.account import facebook
from apps.account import register

class RegisterSerializer(serializers.ModelSerializer):
    """This defines the fields involved in creation of a user

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = User
        fields = ['password','email','role','first_name','last_name']
        extra_kwargs = {
            "password":{"write_only":True}
        }

    def create(self,validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    """This serializes the profile model

    Args:
        serializers ([type]): [description]
    """
    phone_number = PhoneNumberField(region="KE")
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user','avatar','gender','receive_notifications_via_email']

    def update(self,instance):

        instance.phone_number = self.validated_data['phone_number']
        instance.bio = self.validated_data['bio']
        instance.location = self.validated_data['location']
        instance.save()
        return instance

class GetUserSerializer(serializers.ModelSerializer):
    """This deals with getting a user instance

    Args:
        serializers ([type]): [description]
    """
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['email','role','first_name','last_name','member_since','profile']


class SocialLoginSerializer(serializers.Serializer):
    """This handles the user logging in with one of the social login methods

    Args:
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]
        AuthenticationError: [description]
        serializers.ValidationError: [description]

    Returns:
        [type]: [description]
    """
    auth_token = serializers.CharField()

    def google_social_login(self):
        """Thsi handles a login attempt with google as the provider

        Returns:
            [type]: [description]
        """

        provider = AUTH_PROVIDERS.get("google")
        user_data = google.Google.validate(self.validated_data['auth_token'])

        try:
            user_data['sub']
        except Exception as e:
            raise serializers.ValidationError("The token is either invalid or expired")

        if user_data['aud'] != config("GOOGLE_CLIENT_ID"):
            raise AuthenticationError("You are not allowed to perform this action!")

        try:
            user = register.HandleSocialUser.login_social_user(user_data['email'],provider)
            return user

        except Exception as e:
            raise serializers.ValidationError(e)

    def facebook_social_login(self):
        """This handles login via facebook

        Returns:
            [type]: [description]
        """
        provider = AUTH_PROVIDERS.get("facebook")
        user_data = facebook.Facebook.validate(self.validated_data['auth_token'])

        try:
            return register.HandleSocialUser.login_social_user(user_data['email'],provider)

        except Exception as e:
            raise serializers.ValidationError(e)



class SocialSignUpSerializer(serializers.Serializer):
    """This handles a signup with google attempt

    Args:
        serializers ([type]): [description]
    """

    auth_token = serializers.CharField()
    role = serializers.CharField()

    def validate_user_role(self):
        """This handle authenticating the role sent

        Raises:
            ValidationError: [description]
        """
        try:
            role = Role.objects.get(pk = int(self.validated_data['role']))
            return True
        except Role.DoesNotExist:
            raise serializers.ValidationError("The chosen role does not exist")

    def validate_facebook_auth_token(self):
        """This handles a user signup request using facebook
        """
        user_data = facebook.Facebook.validate(self.validated_data['auth_token'])

        provider = AUTH_PROVIDERS.get("facebook")
        role = Role.objects.get(pk = self.validated_data['role'])

        try:
            return register.register_social_user(user_data['email'],user_data['first_name'],user_data['last_name'],role,provider)

        except Exception as e:
            print(e)
            provider = User.objects.get(email = user_data['email']).auth_provider
            raise serializers.ValidationError(f"""The user is already registered, please proceed to login with {provider}""")


    def validate_google_auth_token(self):
        """This handles the actual loggin in

        """
        user_data = google.Google.validate(self.validated_data['auth_token'])

        try:
            user_data['sub']
        except Exception as e:
            raise serializers.ValidationError("The token is either invalid or expired")

        if user_data['aud'] != config("GOOGLE_CLIENT_ID"):
            raise AuthenticationError("You are not allowed to perform this action!")

        try:

            user = User.objects.create(
                email = user_data['email'],
                role = Role.objects.get(pk = self.validated_data['role']),
                first_name = user_data['given_name'],
                last_name = user_data['family_name'],
                auth_provider = AUTH_PROVIDERS.get("google")
            )

            user.set_password(config('SOCIAL_PASSWORD'))
            user.save()
            return User.objects.get(email = user_data['email'])

        except Exception as e:
            provider = User.objects.get(email = user_data['email']).auth_provider
            raise serializers.ValidationError(f"""The user is already registered, please proceed to login with {provider}""")