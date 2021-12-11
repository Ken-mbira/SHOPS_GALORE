from django.contrib import admin

from apps.store.models import *

# Register your models here.
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Attribute)
admin.site.register(Type)
admin.site.register(AttributeValue)
admin.site.register(Category)
