from django.urls import path,include

from apps.store import views

urlpatterns = [
    path("shop/",views.StoreShopListView.as_view(),name="shop_list"),
    path("shop/<int:pk>",views.StoreShopDetailView.as_view(),name="shop_detail"),
    path("product/",views.StoreProductListView.as_view(),name="product_list"),
    path("product/<str:sku>",views.StoreProductDetailView.as_view(),name="product_detail"),
    path("type/",views.StoreTypeView.as_view(),name="type_list"),
    path("brand/",views.StoreBrandView.as_view(),name="brand_list"),
    path("attribute/",views.StoreAttributeView.as_view(),name="attribute_value_list"),
    path("category/",views.CategoryView.as_view(),name="categories"),
    path("location/",views.StoreLocationView.as_view(),name="location"),
]
