import os

from google.oauth2 import service_account

from .base import *  # noqa: F403

MIDDLEWARE.append("api.middleware.RangesMiddleware")  # noqa: F405
CORS_ORIGIN_WHITELIST = ("http://127.0.0.1:3000", "http://0.0.0.0:3000", "http://localhost:3000")
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST

DJANGO_DRF_FILEPOND_STORAGES_BACKEND = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = os.environ.get("BUCKET_NAME", "doccano")
GS_PROJECT_ID = os.environ["GS_PROJECT_ID"]
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
