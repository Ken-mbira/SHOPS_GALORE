from rest_framework import status
from django.urls import reverse

from apps.delivery.tests.test_setup import TestDelivery
from apps.delivery.models import *
from apps.account.models import *
from apps.delivery.serializers import *