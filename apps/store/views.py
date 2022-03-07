from django.shortcuts import render

from rest_framework import permissions
from rest_framework import response
from rest_framework.test import APITestCase
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.store.models import *
from apps.store.serializers import *
from apps.store.permissions import *