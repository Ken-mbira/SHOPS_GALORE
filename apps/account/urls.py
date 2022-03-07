from django.urls import path,include

from apps.account import views

urlpatterns = [
    path('',views.UserView.as_view(),name="create_user"),
    path('instance/',views.UserInstanceView.as_view(),name="user_instance"),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path("google_signup/",views.GoogleSingUpView.as_view(),name="google_signup"),
    path("facebook_signup/",views.FacebookSingUpView.as_view(),name="facebook_signup"),
    path("google_login/",views.GoogleLoginView.as_view(),name="google_login"),
    path("facebook_login/",views.FacebookLoginView.as_view(),name="facebook_login"),
]