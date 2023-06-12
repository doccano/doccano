from .base import *  # noqa: F403
from .base import env

MIDDLEWARE.append("api.middleware.RangesMiddleware")  # noqa: F405

DJANGO_DRF_FILEPOND_STORAGES_BACKEND = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = env("REGION_NAME", "us-west-1")
AWS_STORAGE_BUCKET_NAME = env("BUCKET_NAME", "doccano")
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", None)
AWS_DEFAULT_ACL = "private"
AWS_BUCKET_ACL = "private"
AWS_AUTO_CREATE_BUCKET = True
