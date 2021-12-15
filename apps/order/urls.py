from django.urls import path,include

from apps.order import views

urlpatterns = [
    path("cart/",views.CartView.as_view(),name="cart"),
]
