from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def send_password_reset_email_task(self, user_id, username, email, reset_password_url):
    """
    Celery task to send a password reset email asynchronously.
    """
    try:
        context = {
            'username': username,
            'email': email,
            'reset_password_url': reset_password_url
        }

        email_html_message = render_to_string('emails/password_reset.html', context)
        email_plaintext_message = render_to_string('emails/password_reset.txt', context)

        send_mail(
            "Password Reset for {title}".format(title="AIAgent Platform"),
            email_plaintext_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=email_html_message,
            fail_silently=False,
        )
        logger.info(f"Password reset email task successfully sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send password reset email task to {email}: {str(e)}")
        # Optionally, re-raise the exception for Celery to retry
        raise self.retry(exc=e, countdown=60, max_retries=3)
