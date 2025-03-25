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
        password = getattr(instance, "plain_password", "(Not Available)")
        user_role = "Admin" if instance.is_superuser else "Annotator"
        subject = "Your doccana access credentials! 🦭"
        message = (
            "Welcome to doccana! 😊\n\n"
            "Here are your access credentials to our Doccana web-app:\n\n"
            f"• Username: {instance.username}\n"
            f"• Password: {password}\n\n"
            f"You are an {user_role}.\n\n"
            "Please keep these details in a safe place 🔒. If you have "
            "any doubts or face any issues while logging in, feel free to reach out to us! 📩\n\n"
            "Best regards,\n"
            "The doccana Team 💻✨"
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
