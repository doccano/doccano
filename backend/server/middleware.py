from django.conf import settings
from django.contrib.auth.middleware import RemoteUserMiddleware


def to_django_header(header):
    return f"HTTP_{header.replace('-', '_').upper()}"


class HeaderAuthMiddleware(RemoteUserMiddleware):
    header = to_django_header(settings.HEADER_AUTH_USER_NAME)

    def process_request(self, request):
        if request.user.is_authenticated:
            return

        username = request.META.get(self.header)
        if not username:
            return

        super().process_request(request)
        self.process_user_groups(request.user, request.META)

    @classmethod
    def process_user_groups(cls, user, headers):
        if not user.is_authenticated:
            return

        groups = cls.parse_user_groups_from_header(headers)

        is_superuser = settings.HEADER_AUTH_ADMIN_GROUP_NAME in groups
        if user.is_superuser != is_superuser:
            user.is_superuser = is_superuser
            user.save()

    @classmethod
    def parse_user_groups_from_header(cls, headers):
        try:
            groups_header = headers[to_django_header(settings.HEADER_AUTH_USER_GROUPS)]
        except KeyError:
            return []
        else:
            return groups_header.split(settings.HEADER_AUTH_GROUPS_SEPERATOR)
