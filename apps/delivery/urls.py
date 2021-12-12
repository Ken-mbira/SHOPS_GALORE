from django.urls import path,include

from apps.delivery import views

urlpatterns = [
    path("means/",views.DeliveryMeansView.as_view(),name="means"),
    path("means/<int:id>/",views.UpdateMeans.as_view(),name="means_image"),
]
