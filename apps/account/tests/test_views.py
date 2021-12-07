from apps.account.tests.test_setup import TestSetUp
from rest_framework import status

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