from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    """
    try:
        # send an e-mail to the user
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': "{}?token={}".format(
                instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
                reset_password_token.key)
        }

        email_html_message = render_to_string('emails/password_reset.html', context)
        email_plaintext_message = render_to_string('emails/password_reset.txt', context)

        send_mail(
            # title:
            "Password Reset for {title}".format(title="AIAgent Platform"),
            # message:
            email_plaintext_message,
            # from:
            settings.DEFAULT_FROM_EMAIL,
            # to:
            [reset_password_token.user.email],
            html_message=email_html_message,
            fail_silently=False,
        )
        logger.info(f"Password reset email sent to {reset_password_token.user.email}")
    except Exception as e:
        logger.error(f"Failed to send password reset email to {reset_password_token.user.email}: {str(e)}")
