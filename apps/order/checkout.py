from apps.order.models import *
from datetime import date

import uuid

def cart_to_order(token,id_password,location,phone_number):
    cart = Cart.objects.get(token = token)
    order = Order(owner = cart.owner,id_password = id_password,location = location,phone_number = phone_number)
    order.save()

    for item in cart.cart_items.iterator():
        root_location = item.product.owner.pickup_location.get_root()
        all_children = root_location.get_descendants()
        storage_location = None
        for location in all_children.iterator():
            try:
                storage_location = Storage.objects.get(location = location)
                break
            except:
                continue

        ShopDailyOrders.objects.get_or_create(shop = item.product.owner ,date = date.today(),storage_location = storage_location)
        order_item = OrderItem(
            order = order,
            product = item.product,
            quantity = item.quantity,
            current_price=item.product.price,
            daily_order = ShopDailyOrders.objects.get(shop = item.product.owner ,date = date.today())
        )
        order_item.save()

    cart.complete = True
    cart.save()

    return order