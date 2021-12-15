from django.urls import path,include

from apps.storage import views

urlpatterns = [
    path("",views.StorageView.as_view(),name="storage"),
    path("<int:id>/",views.UpdateStorageView.as_view(),name="update_storage"),
]