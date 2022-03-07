from unicodedata import category
import django_filters

from apps.store.models import *

class ProductFilters(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ['exact'],
            "brand__id": ['exact'],
            "category__id":['exact'],
            "type__id":['exact'],
            "added_on":['lte','gte'],
            "price":['exact','lte','gte'],
            "discount_price":['exact','lte','gte'],
            "volume":['exact','lte','gte'],
            "weight":['exact','lte','gte'],
            "parent__id":['exact'],
            "active":['exact']
        }