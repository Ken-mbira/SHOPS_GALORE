from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from phonenumber_field.modelfields import PhoneNumberField

from apps.account.models import *
from apps.account.emails import send_account_activation_email
from apps.storage.models import *

class RegisterSerializer(serializers.ModelSerializer):
    """This defines the fields involved in creation of a user

    Args:
        serializers ([type]): [description]
    """
    class Meta:
        model = User
        fields = ['password','email','role','first_name','last_name']

    def save(self,request):
        user = User(first_name = self.validated_data['first_name'], last_name=self.validated_data['last_name'],email=self.validated_data['email'],role=self.validated_data['role'])
        user.set_password(self.validated_data['password'])
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        send_account_activation_email(current_site,user)
        return user

class RegisterStaffSerializer(serializers.ModelSerializer):
    """This involves creation of a new staff member

    Args:
        serializers ([type]): [description]

    Raises:
        serializers.ValidationError: [description]
        serializers.ValidationError: [description]

    Returns:
        [type]: [description]
    """
    storage_facility = serializers.IntegerField(required=True)
    class Meta:
        model = User
        fields = ['password','email','role','first_name','last_name','storage_facility']

    def save(self,request):
        storage_facility = StorageFacility.objects.get(pk=self.validated_data['storage_facility'])
        user = User(first_name = self.validated_data['first_name'], last_name=self.validated_data['last_name'],email=self.validated_data['email'],role=self.validated_data['role'])
        user.set_password(self.validated_data['password'])
        user.save()
        staff_profile = StaffProfile.objects.get(user = user)
        staff_profile.storage_facility = storage_facility
        staff_profile.save()
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

class NotificationPreferenceSerializer(serializers.Serializer):
    preference = serializers.BooleanField(required=True,label="The user's preference")

    def change_preference(self,request):
        profile = Profile.objects.get(user = request.user)
        profile.receive_notifications_via_email = self.validated_data['preference']
        profile.save()
        return profile

class ProfilePicSerializer(serializers.Serializer):
    """This handles updating the profile pic of a user

    Args:
        serializers ([type]): [description]
    """
    avatar = serializers.ImageField(required=True)

    def update_profile_pic(self,request):
        profile = Profile.objects.get(user = request.user)
        profile.avatar = self.validated_data['avatar']
        profile.save()
        return profile

class AccountStatusSerializer(serializers.Serializer):
    """This handles activating or deactivating another users account

    Args:
        serializers ([type]): [description]
    """
    user = serializers.CharField(required=True)

    def validate_instance(self):
        """This validates if the user instance is valid
        """
        try:
            User.objects.get(pk = self.validated_data['user'])
            return True
        except:
            raise serializers.ValidationError("The user instance could not be found")

    def deactivate_user(self):
        """this handles deactivation of a user's account
        """
        user = User.objects.get(pk = self.validated_data['user'])
        user.deactivate_account()

    def reinstate_user(self):
        """This handles the reinstation of a user
        """
        user = User.objects.get(pk = self.validated_data['user'])
        user.reinstate()