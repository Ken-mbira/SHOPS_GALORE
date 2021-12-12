from rest_framework.test import APITestCase
from django.urls import reverse

from apps.account.models import *
from apps.store.models import *

class TestDelivery(APITestCase):
    def setUp(self):
        self.register_url = reverse('create_user')
        self.login_url = reverse('login')
        self.auth_url = reverse('token_obtain_pair')
        self.create_shop_url = reverse('new_shop')

        if len(Role.objects.all()) < 4:
            Role.objects.create(name="staff")
            Role.objects.create(name="store_owner")
            Role.objects.create(name="delivery")
            Role.objects.create(name="customer")

        return super().setUp()

    def tearDown(self):
        return super().setUp()