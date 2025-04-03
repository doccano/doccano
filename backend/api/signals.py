from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.utils import timezone

@receiver(user_logged_out)
def update_last_login_on_logout(sender, request, user, **kwargs):
    if user:
        user.last_login = timezone.now()
        user.save()