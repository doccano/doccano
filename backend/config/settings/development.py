from .base import *  # noqa: F403

MIDDLEWARE.append("api.middleware.RangesMiddleware")  # noqa: F405

import dj_database_url

DATABASES = {
    "default": dj_database_url.parse(
        "postgres://doccano_admin:doccano_pass@localhost:5432/doccano?sslmode=disable"
    )
}
