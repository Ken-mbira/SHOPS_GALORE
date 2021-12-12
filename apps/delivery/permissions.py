from rest_framework import permissions,status

class IsDeliveryGuy(permissions.BasePermission):
    """A custom permission to allow only members who have a delivery role to act

    Args:
        permissions ([type]): [description]
    """

    def has_permission(self, request, view):
        if request.user.role.name != "delivery":
            return False
        return True