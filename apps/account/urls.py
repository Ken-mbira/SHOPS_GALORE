from django.urls import path

from apps.account import views

urlpatterns = [
    path('',views.UserView.as_view(),name="create_user"),
    path('login/',views.LoginView.as_view(),name="login"),
    path('login/<token>',views.UserInstanceView.as_view(),name="user_instance"),
]