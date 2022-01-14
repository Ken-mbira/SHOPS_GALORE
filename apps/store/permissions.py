from rest_framework import permissions,status
from rest_framework.exceptions import APIException

from apps.store.models import *

class IsShopOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        try:
            shop = Shop.objects.get(pk = view.kwargs['id'])
            if shop.owner == request.user:
                return True
            return False
        except:
            raise NotFound()

class IsProductOwner(permissions.BasePermission):
    """Only allow owners of a product's shop to edit the product

    Args:
        permissions ([type]): [description]

    Returns:
        [type]: [description]
    """
    def has_permission(self, request, view):
        try:
            product = Product.objects.get(pk = view.kwargs['id'])
            if product.owner.owner == request.user:
                return True
            return False
        except:
            raise NotFound()

class IsImageProductOwner(permissions.BasePermission):
    """
    This only allows owners of a product to change its images
    """
    def has_permission(self, request, view):
        try:
            image = Media.objects.get(pk = view.kwargs['id'])
            if image.product.owner.owner == request.user:
                return True
            return False
        except:
            raise NotFound()
            
class ShopPermissions(permissions.BasePermission):
    """This handles the permissions for handling a shop instance

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.user.role.name != "store_owner":
            return False
        return True

class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"error":True,"message":"What you are looking for was not found"}
    default_code = "not found"