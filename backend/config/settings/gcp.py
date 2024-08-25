from google.oauth2 import service_account

from .base import *  # noqa: F403
from .base import env

MIDDLEWARE.append("api.middleware.RangesMiddleware")  # noqa: F405

DJANGO_DRF_FILEPOND_STORAGES_BACKEND = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = env("BUCKET_NAME", "doccano")
GS_PROJECT_ID = env("GS_PROJECT_ID")

# for more details refer to
# https://django-storages.readthedocs.io/en/latest/backends/gcloud.html#authentication-settings
_google_application_credentials = env("GOOGLE_APPLICATION_CREDENTIALS", "")
if _google_application_credentials:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(_google_application_credentials)
