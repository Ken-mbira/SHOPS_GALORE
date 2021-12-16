from rest_framework import permissions
from rest_framework.exceptions import APIException

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