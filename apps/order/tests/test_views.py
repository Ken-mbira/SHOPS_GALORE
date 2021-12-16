from django.urls import reverse

from rest_framework import status

from apps.order.tests.test_setup import TestOrderSetUp
from apps.order.models import *

class TestOrders(TestOrderSetUp):
    """This tests the flow of a customer ordering an item

    Args:
        TestOrderSetUp ([type]): [description]
    """

    def test_create_cart(self):
        """This tests if a  user can initiate a cart
        """
        response = self.client.post(reverse("cart"))

        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_add_to_cart(self):
        """This tests the add to cart functionality
        """
        token = self.client.post(reverse('cart')).data
        product = Product.objects.get(name="Leather jacket")
        product_info = {
            'product':product.pk
        }
        self.client.credentials(HTTP_CART_TOKEN=token)
        response = self.client.post(reverse("cart_item"),product_info)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        test_cart_item = CartItem.objects.filter(cart = Cart.objects.get(token = token))
        self.assertEqual(test_cart_item[0].product,product)

    def test_transform_cart(self):
        """This test the remove from cart functionality
        """
        token = self.client.post(reverse('cart')).data
        product = Product.objects.get(name="Leather jacket")
        product_info = {
            'product':product.pk
        }
        self.client.credentials(HTTP_CART_TOKEN=token)
        self.client.post(reverse("cart_item"),product_info)
        delivery_information = {
            "id":"12345678",
            "location":"2",
            "phone_number":"+254758926990"
        }
        response = self.client.put(reverse("cart_item"),delivery_information)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        daily_orders = ShopDailyOrders.objects.all()
        self.assertEqual(daily_orders.count(),1)

    def test_add_multiple_to_cart(self):
        """This will test if the user can add multiple objects to their cart
        """
        token = self.client.post(reverse('cart')).data
        product1 = Product.objects.get(name="Leather jacket")
        product_info = {
            'product':product1.pk
        }
        product2 = Product.objects.get(name="Range Rover Sport")
        product2_info = {
            "product":product2.pk
        }
        self.client.credentials(HTTP_CART_TOKEN=token)
        self.client.post(reverse("cart_item"),product_info)
        self.client.post(reverse("cart_item"),product2_info)

        self.assertTrue(CartItem.objects.filter(cart = Cart.objects.get(token=token)).count(),2)

    def transform_cart_with_multiple(self):
        """This checks if the user can checkout with multiple objects in their carts
        """
        token = self.client.post(reverse('cart')).data
        product1 = Product.objects.get(name="Leather jacket")
        product_info = {
            'product':product1.pk
        }
        product2 = Product.objects.get(name="Range Rover Sport")
        product2_info = {
            "product":product2.pk
        }
        self.client.credentials(HTTP_CART_TOKEN=token)
        self.client.post(reverse("cart_item"),product_info)
        self.client.post(reverse("cart_item"),product2_info)

        delivery_information = {
            "id":"12345678",
            "location":"2",
            "phone_number":"+254758926990"
        }
        response = self.client.put(reverse("cart_item"),delivery_information)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertTrue(ShopDailyOrders.objects.all().count() == 2)