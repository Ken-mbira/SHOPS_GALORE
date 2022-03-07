from django.urls import path,include

from apps.store import views

urlpatterns = [
    path("shop/",views.StoreShopListView.as_view(),name="shop_list"),
    path("shop/<int:pk>",views.StoreShopDetailView.as_view(),name="shop_detail"),
]
