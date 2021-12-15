from apps.order.models import *
from datetime import date

def cart_to_order(token,id_password,location):
    cart = Cart.objects.get(token = token)
    order = Order(owner = cart.owner,id_password = id_password,location = location)
    order.save()

    for item in cart.cart_items.iterator():
        ShopDailyOrders.objects.get_or_create(shop = item.product.owner ,date = date.today())
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