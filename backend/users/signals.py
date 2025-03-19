from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(post_save, sender=User)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our Service!'
        message = (
            f"Hello {instance.username},\n\n"
            "Thank you for registering with us. Your account has been successfully created.\n\n"
            "You can now log in and start using our service.\n\n"
            "Best regards,\nThe Team"
        )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
        except BadHeaderError:
            logger.error("Invalid header found while sending email to: %s", instance.email)
        except Exception as e:
            logger.error("Error sending registration email to %s: %s", instance.email, e)