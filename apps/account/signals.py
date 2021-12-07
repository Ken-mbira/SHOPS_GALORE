from apps.account.models import Role
try:
    if len(Role.objects.all()) < 4:
        Role.objects.create(name="staff")
        Role.objects.create(name="store_owner")
        Role.objects.create(name="delivery")
        Role.objects.create(name="customer")
except:
    print("The roles table does not exist yet")