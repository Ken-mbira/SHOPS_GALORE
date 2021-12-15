from django.urls import path,include

from apps.order import views

urlpatterns = [
    path("cart/",views.CartView.as_view(),name="cart"),
    path("cart/item/",views.CartItemView.as_view(),name="cart_item"),
    path("cart/item/<int:id>",views.UpdateCartView.as_view(),name="update_cart"),
]
