from rest_framework import permissions,status
from rest_framework.exceptions import APIException

from apps.store.models import *

class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"error":True,"message":"What you are looking for was not found"}
    default_code = "not found"