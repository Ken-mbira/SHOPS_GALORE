from django.urls import path,include

from apps.store import views

urlpatterns = [
    path("",views.RegisterShopView.as_view(),name="new_shop"),
    path("<int:id>/",views.UpdateShopView.as_view(),name="update"),
    path("delete<int:id>",views.DeleteShopView.as_view(),name="delete"),
    path("product/<int:id>",views.CreateProductView.as_view(),name="new_product"),
    path("brand/",views.BrandView.as_view(),name="brand"),
    path("type/",views.TypeView.as_view(),name="type"),
]
