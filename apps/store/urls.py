from django.urls import path,include

from apps.store import views

urlpatterns = [
    path("shop/",views.StoreShopListView.as_view(),name="shop_list"),
    path("shop/<int:pk>",views.StoreShopDetailView.as_view(),name="shop_detail"),
    path("product/",views.StoreProductListView.as_view(),name="product_list"),
    path("product/<str:sku>",views.StoreProductDetailView.as_view(),name="product_detail"),
]
