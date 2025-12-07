from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
import logging
from ai_agent.profiles.tasks import send_password_reset_email_task

logger = logging.getLogger(__name__)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user via a Celery task
    """
    try:
        reset_password_url = "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key
        )

        send_password_reset_email_task.delay(
            user_id=reset_password_token.user.id,
            username=reset_password_token.user.username,
            email=reset_password_token.user.email,
            reset_password_url=reset_password_url
        )
        logger.info(f"Password reset email task dispatched for user {reset_password_token.user.email}")
    except Exception as e:
        logger.error(f"Failed to dispatch password reset email task for user {reset_password_token.user.email}: {str(e)}")
