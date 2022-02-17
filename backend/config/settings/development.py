from .base import *  # noqa: F403

MIDDLEWARE.append("api.middleware.RangesMiddleware")  # noqa: F405
CORS_ORIGIN_WHITELIST = ("http://127.0.0.1:3000", "http://0.0.0.0:3000", "http://localhost:3000")
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST
