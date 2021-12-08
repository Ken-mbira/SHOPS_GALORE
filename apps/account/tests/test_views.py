from apps.account.tests.test_setup import TestSetUp
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.account.models import *

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

    def test_login_user(self):
        """This tests whether a user can login with correct credentials
        """
        self.client.post(self.register_url,self.user_data)
        res = self.client.post(self.login_url,self.login_credentials)

        self.assertEqual(res.status_code,status.HTTP_200_OK)

        token = Token.objects.get(user = User.objects.get(email = self.login_credentials['email']))

        self.assertEqual(token.key,res.data)

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