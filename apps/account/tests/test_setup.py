from rest_framework.test import APITestCase
from django.urls import reverse

from apps.account.models import *

class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('create_user')
        self.login_url = reverse('login')
        self.auth_url = reverse('token_obtain_pair')
        self.profile_url = reverse('profile')
        self.notification_url = reverse('notification')
        self.deactivate_url = reverse('deactivate')
        self.deactivate_other_url = reverse('deactivate_other')
        self.reinstate_url = reverse('reinstate')

        if len(Role.objects.all()) < 4:
            Role.objects.create(name="staff")
            Role.objects.create(name="store_owner")
            Role.objects.create(name="delivery")
            Role.objects.create(name="customer")

        self.user_data = {
            "password":"1234",
            "first_name":"Kevo",
            "last_name":"cb",
            "email":"kevo@gmail.com",
            "role":2
        }

        self.login_credentials = {
            "email":"kevo@gmail.com",
            "password":"1234"
        }
        return super().setUp()

    def tearDown(self):
        return super().setUp()