from django.contrib import admin

from apps.order.models import *
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
