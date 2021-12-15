from apps.order.models import *
from datetime import date

def cart_to_order(token,id_password):
    cart = Cart.objects.get(token = token)
    order = Order(owner = cart.owner,id_password = id_password)
    order.save()

    for item in cart.cart_items.iterator():
        order_item = OrderItem(
            order = order,
            product = item.product,
            quantity = item.quantity,
            current_price=item.product.price,
            daily_order = ShopDailyOrders.objects.get_or_create(shop = item.product.owner,date = date.today())
        )
        order_item.save()