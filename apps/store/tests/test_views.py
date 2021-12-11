from rest_framework import status

from apps.store.tests.test_setup import TestShop
from apps.store.models import *
from apps.account.models import *

class TestShopViews(TestShop):

    def authenticate(self,user_data):
        response = self.client.post(self.login_url,user_data)
        self.client.credentials(HTTP_AUTHORIZATION = f"Token {response.data}")
        return response

    def test_create_shop(self):
        """This will test if a user who is not a member of the role store owners can create a shop
        """
        non_shop_owner = {
            "password":"1234",
            "first_name":"Kevo",
            "last_name":"cb",
            "email":"kevo@gmail.com",
            "role":3
        }

        new_login_credentials = {
            "email":non_shop_owner['email'],
            "password":non_shop_owner['password']
        }

        self.client.post(self.register_url,non_shop_owner)

        user = User.objects.get(email = new_login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(new_login_credentials)

        response = self.client.post(self.create_shop_url,self.shop_detals)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)