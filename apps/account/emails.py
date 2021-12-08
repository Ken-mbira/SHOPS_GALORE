from django.core.mail import EmailMultiAlternatives
from apps.account.tokens import account_activation_token
from django.conf import settings
from django.template.loader import render_to_string

def send_account_activation_email(current_site,user):
    context = {
        "user":user,
        "domain":current_site.domain,
        "uid":user.pk,
        "token":account_activation_token.make_token(user)
    }

    # render email text
    email_html_message = render_to_string('email/account_activation_email.html', context)
    email_plaintext_message = render_to_string('email/account_activation_email.txt', context)

    msg = EmailMultiAlternatives(
        f"Account activation for {user.first_name}",
        email_plaintext_message,
        f"{settings.EMAIL_HOST_USER}",
        [user.email]
    )

    msg.attach_alternative(email_html_message, "text/html")
    msg.send(fail_silently=True)