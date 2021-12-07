from rest_framework import serializers

from apps.account.models import *

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