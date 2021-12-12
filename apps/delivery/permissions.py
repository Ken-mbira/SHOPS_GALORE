from rest_framework import permissions,status
from rest_framework.exceptions import APIException

from apps.delivery.models import *

class IsDeliveryGuy(permissions.BasePermission):
    """A custom permission to allow only members who have a delivery role to act

    Args:
        permissions ([type]): [description]
    """

    def has_permission(self, request, view):
        if request.user.role.name != "delivery":
            return False
        return True

class IsMeansOwner(permissions.BasePermission):
    """This checks if the user is the owner of the means they are altering

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        try:
            means = DeliveryMeans.objects.get(pk = view.kwargs['id'])
            if means.owner == request.user:
                return True
            return False
        except:
            raise NotFound()

class IsDestinationMeansOwner(permissions.BasePermission):
    """this checks if a user can update set destination for a registered means

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        try:
            destination = Destination.objects.get(pk = view.kwargs['id'])
            if destination.means.owner == request.user:
                return True
            return False
        except:
            raise NotFound()

class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"error":True,"message":"What you are looking for was not found"}
    default_code = "not found"