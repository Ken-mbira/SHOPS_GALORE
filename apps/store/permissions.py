from rest_framework import permissions

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

class ShopPermissions(permissions.BasePermission):
    """This handles the permissions for handling a shop instance

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.user.role.name != "store_owner":
            return False
        return True