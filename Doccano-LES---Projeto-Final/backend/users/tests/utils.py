from django.contrib.auth import get_user_model


def make_user(username: str = "bob", is_staff: bool = False):
    user_model = get_user_model()
    user, _ = user_model.objects.get_or_create(username=username, password="pass", is_staff=is_staff)
    return user
