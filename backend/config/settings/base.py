"""
Django settings for app project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/

Any setting that is configured via an environment variable may
also be set in a `.env` file in the project base directory.
"""
from os import path

import dj_database_url
from environs import Env, EnvError
from furl import furl

# Build paths inside the project like this: path.join(BASE_DIR, ...)
BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

env = Env()
env.read_env(path.join(BASE_DIR, ".env"), recurse=False)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", "v8sk33sy82!uw3ty=!jjv5vp7=s2phrzw(m(hrn^f7e_#1h2al")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", True)

# Application definition
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api",
    "roles",
    "projects",
    "metrics",
    "users",
    "data_import",
    "data_export",
    "auto_labeling",
    "labels",
    "label_types",
    "examples",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "polymorphic",
    "corsheaders",
    "drf_yasg",
    "dj_rest_auth",
    "django_celery_results",
    "django_drf_filepond",
    "health_check",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.celery",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]


ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Django templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [path.join(BASE_DIR, "client/dist")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    path.join(BASE_DIR, "client/dist/static"),
]
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Auth settings
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
HEADER_AUTH_USER_NAME = env("HEADER_AUTH_USER_NAME", "")
HEADER_AUTH_USER_GROUPS = env("HEADER_AUTH_USER_GROUPS", "")
HEADER_AUTH_ADMIN_GROUP_NAME = env("HEADER_AUTH_ADMIN_GROUP_NAME", "")
HEADER_AUTH_GROUPS_SEPERATOR = env("HEADER_AUTH_GROUPS_SEPERATOR", default=",")
if HEADER_AUTH_USER_NAME and HEADER_AUTH_USER_GROUPS and HEADER_AUTH_ADMIN_GROUP_NAME:
    MIDDLEWARE.append("api.middleware.HeaderAuthMiddleware")
    AUTHENTICATION_BACKENDS.append("django.contrib.auth.backends.RemoteUserBackend")

# Role settings
ROLE_PROJECT_ADMIN = env("ROLE_PROJECT_ADMIN", "project_admin")
ROLE_ANNOTATOR = env("ROLE_ANNOTATOR", "annotator")
ROLE_ANNOTATION_APPROVER = env("ROLE_ANNOTATION_APPROVER", "annotation_approver")

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": env.int("DOCCANO_PAGE_SIZE", default=5),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "SEARCH_PARAM": "q",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_xml.renderers.XMLRenderer",
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Testing
TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"
TEST_OUTPUT_DIR = path.join(BASE_DIR, "junitxml")

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/projects/"
LOGOUT_REDIRECT_URL = "/"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": path.join(BASE_DIR, "db.sqlite3"),
    }
}
# Change 'default' database configuration with $DATABASE_URL.
DATABASES["default"].update(
    dj_database_url.config(
        env="DATABASE_URL",
        conn_max_age=env.int("DATABASE_CONN_MAX_AGE", 500),
        ssl_require="sslmode" not in furl(env("DATABASE_URL", "")).args,
    )
)

# work-around for dj-database-url: explicitly disable ssl for sqlite
if DATABASES["default"].get("ENGINE") == "django.db.backends.sqlite3":
    DATABASES["default"].get("OPTIONS", {}).pop("sslmode", None)

# work-around for dj-database-url: patch ssl for mysql
if DATABASES["default"].get("ENGINE") == "django.db.backends.mysql":
    DATABASES["default"].get("OPTIONS", {}).pop("sslmode", None)
    if env("MYSQL_SSL_CA", None):
        DATABASES["default"].setdefault("OPTIONS", {}).setdefault("ssl", {}).setdefault("ca", env("MYSQL_SSL_CA", None))

# default to a sensible modern driver for Azure SQL
if DATABASES["default"].get("ENGINE") == "sql_server.pyodbc":
    DATABASES["default"].setdefault("OPTIONS", {}).setdefault("driver", "ODBC Driver 17 for SQL Server")


# Sessions and CSRF
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", False)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", False)
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", [])

# Allow all host headers
ALLOWED_HOSTS = ["*"]

# Batch size for importing data
IMPORT_BATCH_SIZE = env.int("IMPORT_BATCH_SIZE", 1000)

# Necessary for email verification of new accounts
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", False)
EMAIL_HOST = env("EMAIL_HOST", None)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", None)
EMAIL_PORT = env.int("EMAIL_PORT", 587)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "webmaster@localhost")
if not EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# User media files
MEDIA_ROOT = env("MEDIA_ROOT", path.join(BASE_DIR, "media"))
MEDIA_URL = "/media/"

# Filepond settings
DJANGO_DRF_FILEPOND_UPLOAD_TMP = path.join(BASE_DIR, "filepond-temp-uploads")
DJANGO_DRF_FILEPOND_FILE_STORE_PATH = MEDIA_ROOT

# Celery settings
DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191
CELERY_RESULT_BACKEND = "django-db"
try:
    CELERY_BROKER_URL = env("CELERY_BROKER_URL")
except EnvError:
    try:
        # quickfix for Heroku.
        # See https://github.com/doccano/doccano/issues/1327.
        uri = env("DATABASE_URL")
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        CELERY_BROKER_URL = "sqla+{}".format(uri)
    except EnvError:
        CELERY_BROKER_URL = "sqla+sqlite:///{}".format(DATABASES["default"]["NAME"])
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
