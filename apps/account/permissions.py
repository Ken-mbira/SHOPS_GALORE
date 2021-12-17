from rest_framework import permissions,status
from rest_framework.exceptions import APIException

from apps.storage.models import StorageFacility

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class IsStaff(permissions.BasePermission):
    """This checks if a user making a request is a staff member

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.user.role.name == "staff":
            return True
        return False

class CheckRole(permissions.BasePermission):
    """This disables registration of a staff user via the registration endpoint

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.data['role'] == "1":
            return False
        return True

class CheckRegisterNewStaff(permissions.BasePermission):
    """These are the checks when creating a new staff member

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.user.role.name != "staff":
            return False
        
        try:
            StorageFacility.objects.get(pk = request.data['storage_facility'])
            return True
        except Exception as e:
            print(e)
            raise StorageNotFound()

class StorageNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"error":True,"message":"What you are looking for was not found"}
    default_code = "not found"