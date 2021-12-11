from rest_framework import status
from django.urls import reverse

from apps.store.tests.test_setup import TestShop
from apps.store.models import *
from apps.account.models import *
from apps.store.serializers import *

class TestShopViews(TestShop):

    def authenticate(self,user_data):
        response = self.client.post(self.login_url,user_data)
        self.client.credentials(HTTP_AUTHORIZATION = f"Token {response.data}")
        return response

    def test_non_shop_user_create_shop(self):
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

    def test_create_shop(self):
        """This will test if a user can create a shop
        """

        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        response = self.client.post(self.create_shop_url,self.shop_detals)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_shops(self):
        """This will test if a shop's profile can be updated by a user
        """

        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        self.client.post(self.create_shop_url,self.shop_detals)

        response = self.client.get(self.create_shop_url)

        correct_instance = ShopSerializer(Shop.objects.filter(owner = User.objects.get(email = self.login_credentials['email'])),many=True).data
        self.assertEqual(response.data,correct_instance)

    def test_update_shop(self):
        """This will test if the shop's owner can update the shop profile
        """
        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        created_shop = self.client.post(self.create_shop_url,self.shop_detals)

        new_shop_profile = {
            "name": "Maendeleo developers",
            "bio": "A new company slogan",
            "pickup_location": "string",
            "phone_contact": "+254722442604",
            "email_contact": "mbira@ken.com"
        }

        response = self.client.put(reverse('update',kwargs={"id":created_shop.data['id']}),new_shop_profile)

        self.assertEqual(response.status_code,status.HTTP_200_OK)