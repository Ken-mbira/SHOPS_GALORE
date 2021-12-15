from rest_framework import permissions,status

from rest_framework.exceptions import APIException

class IsBuyerPermission(permissions.BasePermission):
    """This checks if a user is a buyer

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True

        elif request.user.role.name == "customer":
            return True
        else:
            return False

class CheckCart(permissions.BasePermission):
    """This will check if the cart is being updated the token is provided

    Args:
        permissions ([type]): [description]
    """
    def has_permission(self, request, view):
        if request.method == 'PUT':
            if request.META.get('HTTP_CART_TOKEN'):
                return True
            else:
                raise NoCart()

        elif request.method == 'GET':
            if request.user.is_authenticated:
                return True
            raise IsAuthenticatedCustomer()

        else:
            return True

class NoCart(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"message":"Your cart details were not provided"}
    default_code = "no cart token"

class IsAuthenticatedCustomer(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"message":"You are not authorised to perform this action"}
    default_code = "not authenticated"