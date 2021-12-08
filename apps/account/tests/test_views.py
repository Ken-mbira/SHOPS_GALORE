from apps.account.tests.test_setup import TestSetUp
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core import mail

from apps.account.models import *
from apps.account.serializers import *

class TestViews(TestSetUp):
    def test_roles(self):
        self.assertEqual(Role.objects.all().count(),4)

    def test_create_user(self):
      """
      This tests whether a user can register in the website"""
      res = self.client.post(self.register_url,self.user_data)
      self.assertEqual(res.status_code,status.HTTP_200_OK)
      user = User.objects.get(email = self.user_data['email'])
      self.assertEqual(user.first_name,self.user_data['first_name'])

    def test_login_user_without_activation(self):
        """This tests whether a user can login while not activated account
        """
        self.client.post(self.register_url,self.user_data)
        res = self.client.post(self.login_url,self.login_credentials)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_user_activation(self):
        """This will test whether a user receives an account activation email
        """
        self.client.post(self.register_url,self.user_data)
        self.assertEqual(len(mail.outbox), 1)

    def test_wrong_login_user(self):
        """This tests whether a user can login with incorrect credentials
        """
        wrong_credentials = {
            "email":"wrong@credentials.com",
            "password":"wrong"
        }
        self.client.post(self.register_url,self.user_data)
        res = self.client.post(self.login_url,wrong_credentials)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_get_user_instance(self):
        """This tests whether the get user instance endpoint returns a user instance
        """
        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        correct_instance = GetUserSerializer(User.objects.get(email = self.login_credentials['email'])).data

        token = self.client.post(self.login_url,self.login_credentials).data
        instance = self.client.get(self.login_url + f"{token}")
        self.assertEqual(correct_instance,instance.data)  

    def authenticate(self,user_data):
        response = self.client.post(self.login_url,user_data)
        self.client.credentials(HTTP_AUTHORIZATION = f"Token {response.data}")

    def test_update_profile(self):
        """This test whether a user can update their own profile
        """
        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        new_profile = {
            "bio":"This is my new bio",
            "phone_number":"+254722123456",
            "location":"Kiserian"
        }

        self.client.put(self.profile_url,new_profile)

        self.assertEqual(User.objects.get(email = self.login_credentials['email']).profile.bio,new_profile['bio'])

    def test_get_profile(self):
        """This checks if a user can view their own profile
        """
        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        correct_instance = ProfileSerializer(Profile.objects.get(user = user)).data

        instance = self.client.get(self.profile_url)

        self.assertEqual(instance.data,correct_instance)

    def test_change_notification_preference(self):
        """This test whether a user can change their notification preference
        """
        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        new_preference = {
            "preference":False
        }

        self.client.put(self.notification_url,new_preference)
        self.assertEqual(User.objects.get(email = self.login_credentials['email']).profile.receive_notifications_via_email,new_preference['preference'])

        other_preference = {
            "preference":False
        }

        self.client.put(self.notification_url,other_preference)
        self.assertEqual(User.objects.get(email = self.login_credentials['email']).profile.receive_notifications_via_email,other_preference['preference'])