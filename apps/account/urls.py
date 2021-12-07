from django.urls import path

from apps.account import views

urlpatterns = [
    path('',views.UserView.as_view(),name="list_create_user")
]