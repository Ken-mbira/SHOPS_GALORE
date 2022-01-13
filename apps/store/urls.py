from django.urls import path,include

from apps.store import views

urlpatterns = [
    path("",views.RegisterShopView.as_view(),name="new_shop"),
    path("<int:id>/",views.UpdateShopView.as_view(),name="update"),
    path("<int:id>/product/",views.ShopProductView.as_view(),name="products"),
    path("delete/<int:id>",views.DeleteShopView.as_view(),name="delete"),
    path("new_single_product/<int:id>",views.CreateSingleProductView.as_view(),name="new_single_product"),
    path("new_parent_product/<int:id>",views.CreateParentProductView.as_view(),name="new_parent_product"),
    path("new_child_product/<int:id>",views.CreateChildProductView.as_view(),name="new_child_product"),
    path("brand/",views.BrandView.as_view(),name="brand"),
    path("type/",views.TypeView.as_view(),name="type"),
    path("product/<int:id>",views.SingleProductView.as_view(),name="product"),
    path("product/stock/<int:id>/",views.StockView.as_view(),name="stock"),
    path("product/image/<int:id>/",views.UpdateDefaultImage.as_view(),name="update_default_image"),
    path("attribute/<int:id>",views.AttributeFilterView.as_view(),name="attribute"),
    path("product/review/<int:id>/",views.ReviewView.as_view(),name="review"),
    path("category/",views.CategoryView.as_view(),name="categories"),
]
