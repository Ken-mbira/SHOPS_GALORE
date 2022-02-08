from apps.account.models import *
from decouple import config


def register_social_user(email,first_name,last_name,role,auth_provider):
    user = User.objects.create(
        email = email,
        role = role,
        first_name = first_name,
        last_name = last_name,
        auth_provider = auth_provider
    )

    user.set_password(config('SOCIAL_PASSWORD'))
    user.save()
    return User.objects.get(email = email)