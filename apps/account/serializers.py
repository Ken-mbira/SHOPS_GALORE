from rest_framework import serializers

from apps.account.models import *
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    """This defines the fields involved in creation of a user

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = User
        fields = ['password','email','role','first_name','last_name']

    def save(self):
        user = User(first_name = self.validated_data['first_name'], last_name=self.validated_data['last_name'],email=self.validated_data['email'],role=self.validated_data['role'])
        user.set_password(self.validated_data['password'])
        user.save()
        return user

class RoleSerializer(serializers.ModelSerializer):
    """This deals with serializing the user roles

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Role
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    """This serializes the profile model

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = Profile
        fields = '__all__'

class GetUserSerializer(serializers.ModelSerializer):
    """This deals with getting a user instance

    Args:
        serializers ([type]): [description]
    """
    role = RoleSerializer()
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['email','role','first_name','last_name','member_since','profile']


class LoginSerializer(serializers.Serializer):
    """This defines the functions in the login function

    Args:
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,required=True)

    def validate_user(self):
        """This handles the validation of the user

        Raises:
            serializers.ValidationError: [description]
        """
        user = authenticate(email = self.validated_data['email'],password = self.validated_data['password'])

        if user is not None:
            return user

        else:
            raise serializers.ValidationError('The user could not be validated with the provided credentials.')