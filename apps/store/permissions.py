from rest_framework import permissions

from apps.store.models import *

class IsShopOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        # print(dir(view))
        # print(view.kwargs)
        try:
            shop = Shop.objects.get(pk = view.kwargs['id'])
            if shop.owner == request.user:
                return True
            return False
        except:
            pass
        
class ShopPermissions(permissions.BasePermission):
    """This handles the permissions for handling a shop instance

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.user.role.name != "store_owner":
            return False
        return True