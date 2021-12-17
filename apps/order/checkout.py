from apps.order.models import *
from datetime import date

import uuid

from apps.storage.models import StorageFacility

def get_storage_location(location):
    """This will return a storage location whose location is a child of the provided location

    Args:
        location ([type]): [description]
    """
    all_children = location.get_descendants()
    for location in all_children.iterator():
        try:
            storage_location = StorageFacility.objects.get(location = location)
            break
        except:
            storage_location = None
            continue

    return storage_location

def cart_to_order(token,id_password,location,phone_number):
    cart = Cart.objects.get(token = token)
    order = Order(owner = cart.owner,id_password = id_password,location = location,phone_number = phone_number)
    order.save()

    for item in cart.cart_items.iterator():
        root_location = item.product.owner.pickup_location.get_root()
        storage_location = get_storage_location(root_location)

        order_item = OrderItem(
            order = order,
            product = item.product,
            quantity = item.quantity,
            current_price=item.product.price,
            daily_order = ShopDailyOrders.objects.get_or_create(shop = item.product.owner ,date = date.today(),storage_location = storage_location)[0]
        )
        order_item.save()

        if order_item.requires_transit:
            order_item.transit = DailyTransit.objects.get_or_create(start_location = storage_location,end_location = get_storage_location(order.location),created_on = datetime.now())[0]
            order_item.save()

    cart.complete = True
    cart.save()

    return order