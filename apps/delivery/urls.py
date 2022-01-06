from django.urls import path,include

from apps.delivery import views

urlpatterns = [
    path("means/",views.DeliveryMeansView.as_view(),name="means"),
    path("means/<int:id>/",views.UpdateMeans.as_view(),name="means_image"),
    path("destination/<int:id>/",views.DestinationView.as_view(),name="destination"),
    path("location/",views.LocationView.as_view(),name="locations"),
]
