from apps.account.models import *
try:
    if len(Role.objects.all()) < 4:
        Role.objects.create(name="staff")
        Role.objects.create(name="store_owner")
        Role.objects.create(name="delivery")
        Role.objects.create(name="customer")
except:
    print("The roles table does not exist yet")

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_associate_tables(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)