from rest_framework import permissions

class ShopPermissions(permissions.BasePermission):
    """This handles the permissions for handling a shop instance

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.user.role.name != "store_owner":
            return False
        return True