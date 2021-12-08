from django.urls import path,include

from apps.account import views

urlpatterns = [
    path('',views.UserView.as_view(),name="create_user"),
    path('login/',views.LoginView.as_view(),name="login"),
    path('login/<token>',views.UserInstanceView.as_view(),name="user_instance"),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('profile/',views.ProfileView.as_view(),name="profile"),
    path('notification_preference/',views.ToggleNotificationView.as_view(),name="notification"),
    path('profile_pic/',views.UpdateProfilePic.as_view(),name="profile_pic"),
]