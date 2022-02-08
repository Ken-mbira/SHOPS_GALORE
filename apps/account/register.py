from decouple import config

from apps.account.models import *
from django.contrib.auth import authenticate


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
# test
class HandleSocialUser:

    def login_social_user(email,provider):
        """This handles a user's attempt to login using the social login options

        Args:
            email ([type]): [description]
            provider ([type]): [description]
        """
        user = authenticate(email= email,password = config("SOCIAL_PASSWORD"))

        if user is None:
            raise Exception("No account was found with the given credentials!")

        if user.auth_provider != provider:
            raise Exception(f"""You have used a different provider for your account. Please proceed to login using {provider}""")

        return user