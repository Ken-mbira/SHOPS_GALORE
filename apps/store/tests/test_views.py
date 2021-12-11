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

        response = self.client.post(self.create_shop_url,self.shop_details)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_create_shop(self):
        """This will test if a user can create a shop
        """

        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        response = self.client.post(self.create_shop_url,self.shop_details)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_shops(self):
        """This will test if a shop's profile can be updated by a user
        """

        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        self.client.post(self.create_shop_url,self.shop_details)

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

        created_shop = self.client.post(self.create_shop_url,self.shop_details)

        new_shop_profile = {
            "name": "Maendeleo developers",
            "bio": "A new company slogan",
            "pickup_location": "string",
            "phone_contact": "+254722442604",
            "email_contact": "mbira@ken.com"
        }

        response = self.client.put(reverse('update',kwargs={"id":created_shop.data['id']}),new_shop_profile)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_update_others_shop(self):
        """This test checks if a user can update a shop that's not his'hers
        """
        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        shop = Shop(
            name = self.shop_details['name'],
            bio = self.shop_details['bio'],
            owner = User.objects.get(email = self.login_credentials['email']),
            pickup_location = self.shop_details['pickup_location'],
            email_contact = self.shop_details['email_contact'],
        )
        shop.save()

        other_user_credentials = {
            "password":"1234",
            "first_name":"Musa",
            "last_name":"Mosomi",
            "email":"mosomi@gmail.com",
            "role":2
        }

        other_user_login_credentials = {
            "email":other_user_credentials['email'],
            "password":other_user_credentials['password']
        }

        self.client.post(self.register_url,other_user_credentials)

        user = User.objects.get(email = other_user_login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(other_user_login_credentials)

        new_shop_profile = {
            "name": "Maendeleo developers",
            "bio": "A new company slogan",
            "pickup_location": "string",
            "phone_contact": "+254722442604",
            "email_contact": "mbira@ken.com"
        }

        response = self.client.put(reverse('update',kwargs={"id":shop.pk}),new_shop_profile)

        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_update_non_existing_shop(self):
        """This test checks if a user can update a shop that does not exist
        """
        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        shop = Shop(
            name = self.shop_details['name'],
            bio = self.shop_details['bio'],
            owner = User.objects.get(email = self.login_credentials['email']),
            pickup_location = self.shop_details['pickup_location'],
            email_contact = self.shop_details['email_contact'],
        )
        shop.save()

        other_user_credentials = {
            "password":"1234",
            "first_name":"Musa",
            "last_name":"Mosomi",
            "email":"mosomi@gmail.com",
            "role":2
        }

        other_user_login_credentials = {
            "email":other_user_credentials['email'],
            "password":other_user_credentials['password']
        }

        self.client.post(self.register_url,other_user_credentials)

        user = User.objects.get(email = other_user_login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(other_user_login_credentials)

        new_shop_profile = {
            "name": "Maendeleo developers",
            "bio": "A new company slogan",
            "pickup_location": "string",
            "phone_contact": "+254722442604",
            "email_contact": "mbira@ken.com"
        }

        response = self.client.put(reverse('update',kwargs={"id":100}),new_shop_profile)

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_delete_shop(self):
        """This will test if a user can delete their own shop
        """

        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        created_shop = self.client.post(self.create_shop_url,self.shop_details)
        
        response = self.client.delete(reverse('update',kwargs={"id":created_shop.data['id']}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(False,(Shop.objects.get(pk = created_shop.data['id']).functional and Shop.objects.get(pk = created_shop.data['id']).active))

    def test_delete_others_shop(self):
        """This test checks if a user can update a shop that's not his'hers
        """
        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        shop = Shop(
            name = self.shop_details['name'],
            bio = self.shop_details['bio'],
            owner = User.objects.get(email = self.login_credentials['email']),
            pickup_location = self.shop_details['pickup_location'],
            email_contact = self.shop_details['email_contact'],
        )
        shop.save()

        other_user_credentials = {
            "password":"1234",
            "first_name":"Musa",
            "last_name":"Mosomi",
            "email":"mosomi@gmail.com",
            "role":2
        }

        other_user_login_credentials = {
            "email":other_user_credentials['email'],
            "password":other_user_credentials['password']
        }

        self.client.post(self.register_url,other_user_credentials)

        user = User.objects.get(email = other_user_login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(other_user_login_credentials)

        new_shop_profile = {
            "name": "Maendeleo developers",
            "bio": "A new company slogan",
            "pickup_location": "string",
            "phone_contact": "+254722442604",
            "email_contact": "mbira@ken.com"
        }

        response = self.client.delete(reverse('update',kwargs={"id":shop.pk}),new_shop_profile)

        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_delete_non_existent_shop(self):
        """This will test if a user can delete their own shop
        """

        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        created_shop = self.client.post(self.create_shop_url,self.shop_details)
        
        response = self.client.delete(reverse('update',kwargs={"id":10000}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_full_delete_shop(self):
        """This will test if a user can delete their own shop
        """

        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        created_shop = self.client.post(self.create_shop_url,self.shop_details)
        
        response = self.client.delete(reverse('delete',kwargs={"id":created_shop.data['id']}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(User.objects.get(email = self.login_credentials['email']).shops.all().count(),0)

    def test_create_product(self):
        """This will test if a product can be created for the first time
        """
        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(self.login_credentials)

        shop = self.client.post(self.create_shop_url,self.shop_details)

        self.assertEqual(Product.objects.all().count(),0)

        response = self.client.post(reverse('new_product',kwargs={"id":shop.data['id']}),self.product_details)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        self.assertEqual(Product.objects.all().count(),1)

    def test_create_product_in_others_shop(self):
        """This test checks if a user can create a product in a shop that's not his'hers
        """
        self.client.post(self.register_url,self.user_data)

        user = User.objects.get(email = self.login_credentials['email'])
        user.is_active = True
        user.save()

        shop = Shop(
            name = self.shop_details['name'],
            bio = self.shop_details['bio'],
            owner = User.objects.get(email = self.login_credentials['email']),
            pickup_location = self.shop_details['pickup_location'],
            email_contact = self.shop_details['email_contact'],
        )
        shop.save()

        other_user_credentials = {
            "password":"1234",
            "first_name":"Musa",
            "last_name":"Mosomi",
            "email":"mosomi@gmail.com",
            "role":2
        }

        other_user_login_credentials = {
            "email":other_user_credentials['email'],
            "password":other_user_credentials['password']
        }

        self.client.post(self.register_url,other_user_credentials)

        user = User.objects.get(email = other_user_login_credentials['email'])
        user.is_active = True
        user.save()

        self.authenticate(other_user_login_credentials)

        response = self.client.post(reverse('new_product',kwargs={"id":shop.pk}),self.product_details)

        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)