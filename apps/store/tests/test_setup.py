from rest_framework.test import APITestCase
from django.urls import reverse

from apps.account.models import *
from apps.store.models import *

class TestShop(APITestCase):
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

        self.product_type = Type.objects.create(name = "Clothing")
        self.product_brand = Brand.objects.create(name="Gucci")
        self.first_category = Category.objects.create(name = "Clothing")
        self.child_category = Category.objects.create(name="Men's Clothing",parent = self.first_category)
        self.product_attribute = Attribute.objects.create(name="Size",description = "The size of a product")
        self.product_attribute.type.add(self.product_type)
        self.product_attribute.save()
        self.large_attribute = AttributeValue.objects.create(value="large",attribute = self.product_attribute,description = "The biggest of the sizes")
        self.middle_attribute = AttributeValue.objects.create(value="middle",attribute = self.product_attribute,description = "The middle of the sizes")
        self.small_attribute = AttributeValue.objects.create(value="small",attribute = self.product_attribute,description = "The least of the sizes")
        self.parent_location = Location.objects.create(name="Kajiado")
        self.location = Location.objects.create(name="Kiserian",parent = self.parent_location)


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

        self.shop_details = {
            "name": "Jitihada developers",
            "bio": "string",
            "pickup_location": 1,
            "phone_contact": "+254722442604",
            "email_contact": "mbira@ken.com"
        }

        self.single_product_details = {
            "name": "Mens Leather Jacket",
            "brand": 1,
            "category": 1,
            "type": 1,
            "description": "A leather jacket for men",
            "price": "12.50",
            "volume":100,
            "sku":"asdfafdadf"
        }
        return super().setUp()

    def tearDown(self):
        return super().setUp()