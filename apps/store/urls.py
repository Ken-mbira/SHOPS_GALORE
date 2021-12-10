from django.urls import path,include

from apps.store import views

urlpatterns = [
    path("register/",views.RegisterShop.as_view(),name="new_shop"),
]
