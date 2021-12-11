from django.urls import path,include

from apps.store import views

urlpatterns = [
    path("",views.RegisterShopView.as_view(),name="new_shop"),
    path("<int:id>/",views.UpdateShopView.as_view(),name="update"),
]
