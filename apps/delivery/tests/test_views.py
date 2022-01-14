from rest_framework import status
from django.urls import reverse

from apps.delivery.tests.test_setup import TestDelivery
from apps.delivery.models import *
from apps.account.models import *
from apps.delivery.serializers import *

class TestShopViews(TestDelivery):

    def authenticate(self,user_data):
        response = self.client.post(self.auth_url,user_data)
        try:
            self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {response.data['access']}")
        except :
            return response

    def test_register_means(self):
        """this tests whether a user can register a new means
        """