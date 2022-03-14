from django.urls import path,include

from apps.delivery import views

urlpatterns = [
    path("means/",views.DeliveryMeansView.as_view(),name="means_list"),
    path("location/",views.DeliveryLocationView.as_view(),name="location_list"),
    path("register_means/",views.DeliveryRegisteredMeansListView.as_view(),name="registered_means_list"),
    path("register_means/<int:pk>",views.DeliveryRegisteredMeansDetailView.as_view(),name="registered_means_detail"),
    path("register_means/image/<int:pk>",views.DeliveryRegisteredMeansImageDetailView.as_view(),name="registered_means_image"),
    path("destination/",views.DeliveryDestinationListView.as_view(),name="delivery_list"),
    path("destination/<int:pk>",views.DeliveryDestinationDetailView.as_view(),name="delivery_detail"),
]
