from rest_framework.test import APITestCase
from django.urls import reverse

from apps.account.models import *

class TestShop(APITestCase):
    def setUp(self):
        self.register_url = reverse('create_user')
        self.login_url = reverse('login')
        self.create_shop_url = reverse('new_shop')

        if len(Role.objects.all()) < 4:
            Role.objects.create(name="staff")
            Role.objects.create(name="store_owner")
            Role.objects.create(name="delivery")
            Role.objects.create(name="customer")

        self.user_data = {
            "password":"1234",
            "first_name":"Marko",
            "last_name":"Awan",
            "email":"awan@gmail.com",
            "role":2
        }

        self.login_credentials = {
            "email":"awan@gmail.com",
            "password":"1234"
        }

        self.shop_detals = {
            "name": "Jitihada developers",
            "bio": "string",
            "pickup_location": "string",
            "phone_contact": "+254722442604",
            "email_contact": "mbira@ken.com"
        }
        return super().setUp()

    def tearDown(self):
        return super().setUp()