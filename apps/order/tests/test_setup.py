from django.urls import reverse

from rest_framework.test import APITestCase

from apps.account.models import *
from apps.store.models import *
from apps.order.models import *

class TestOrderSetUp(APITestCase):
    """These test the flow of a user creating a cart of products and making an order

    Args:
        APITestCase ([type]): [description]
    """
    def setUp(self):
        self.register_url = reverse('create_user')
        self.auth_url = reverse('token_obtain_pair')

        if len(Role.objects.all()) < 4:
            Role.objects.create(name="staff")
            Role.objects.create(name="store_owner")
            Role.objects.create(name="delivery")
            Role.objects.create(name="customer")

        zone1 = Location(name="zone1")
        zone1.save()
        kajiado = Location(name="Kajiado",parent = zone1)
        kajiado.save()
        kiserian = Location(name="kiserian",parent=kajiado)
        kiserian.save()

        Storage.objects.create(name="Last heath",location = kiserian)

        Brand.objects.create(name="Gucci")

        clothing_category = Category(name="Clothing")
        clothing_category.save()
        men_clothing = Category(name="mens clothing",parent = clothing_category)
        men_clothing.save()

        cars_category = Category(name="Cars")
        cars_category.save()
        luxury_cars = Category(name="Luxury Cars",parent=cars_category)

        clothing_type = Type(name="Clothing",description="Everything wearable")
        clothing_type.save()

        cars_type = Type(name="cars",description="Everything on wheels")
        cars_type.save()

        size_attribute = Attribute(name="size",description="How big something is")
        size_attribute.save()
        size_attribute.type.add(clothing_type)
        size_attribute.save()
        size_attribute.type.add(cars_type)
        size_attribute.save()

        large_size = AttributeValue(value="large",attribute=size_attribute,description="The largest size available")
        large_size.save()


        User.objects.create(
            email="first@store.com",
            role = Role.objects.get(name="store_owner"),
            first_name = "John",
            last_name = "Doe",
        )

        Shop.objects.create(
            name="Mavazi Corp",
            bio = "dedicated to style",
            owner = User.objects.get(email="first@store.com"),
            pickup_location = kiserian,
            phone_contact = "+254758926990",
            email_contact = "mavazi@corp.com",
        )

        Product.objects.create(
            name="Leather jacket",
            brand = Brand.objects.get(name="Gucci"),
            category = men_clothing,
            type=clothing_type,
            owner = Shop.objects.get(email_contact="mavazi@corp.com"),
            description = "Keep warm this winter",
            price="12.50"
        )

        stock = Stock.objects.get(product = Product.objects.get(name="Leather jacket"))

        stock.count += 2
        stock.last_stock_check_date = datetime.now()
        stock.save()

        Shop.objects.create(
            name="Magari Kibao",
            bio = "Drive class",
            owner = User.objects.get(email="first@store.com"),
            pickup_location = kiserian,
            phone_contact = "+254758926990",
            email_contact = "magari@kibao.com",
        )

        Product.objects.create(
            name="Range Rover Sport",
            brand = Brand.objects.get(name="Gucci"),
            category = cars_category,
            type=cars_type,
            owner = Shop.objects.get(email_contact="mavazi@corp.com"),
            description = "Keep warm this winter",
            price="12.50"
        )

        stock = Stock.objects.get(product = Product.objects.get(name="Range Rover Sport"))

        stock.count += 2
        stock.last_stock_check_date = datetime.now()
        stock.save()


        customer_data = {
            "password":"1234",
            "first_name":"Machel",
            "last_name":"Mwokovu",
            "email":"mwokovu@gmail.com",
            "role":3
        }


        return super().setUp()

    def tearDown(self) -> None:
        return super().setUp()