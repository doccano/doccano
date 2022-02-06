from django.contrib.auth import get_user_model


def make_user(username: str = "bob"):
    user_model = get_user_model()
    user, _ = user_model.objects.get_or_create(username=username, password="pass")
    return user
