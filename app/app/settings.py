"""
Django settings for app project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/

Any setting that is configured via an environment variable may
also be set in a `.env` file in the project base directory.
"""
import importlib.util
import sys
from os import path

import dj_database_url
from environs import Env
from furl import furl


# Build paths inside the project like this: path.join(BASE_DIR, ...)
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

env = Env()
env.read_env(path.join(BASE_DIR, '.env'), recurse=False)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY',
                 'v8sk33sy82!uw3ty=!jjv5vp7=s2phrzw(m(hrn^f7e_#1h2al')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', True)

# True if you want to allow users to be able to create an account
ALLOW_SIGNUP = env.bool('ALLOW_SIGNUP', True)

# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'social_django',
    'polymorphic',
    'corsheaders',
    'drf_yasg'
]

CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER = env('CLOUD_BROWSER_LIBCLOUD_PROVIDER', None)
CLOUD_BROWSER_APACHE_LIBCLOUD_ACCOUNT = env('CLOUD_BROWSER_LIBCLOUD_ACCOUNT', None)
CLOUD_BROWSER_APACHE_LIBCLOUD_SECRET_KEY = env('CLOUD_BROWSER_LIBCLOUD_KEY', None)

if CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER:
    CLOUD_BROWSER_DATASTORE = 'ApacheLibcloud'
    CLOUD_BROWSER_OBJECT_REDIRECT_URL = '/v1/cloud-upload'
    INSTALLED_APPS.append('cloud_browser')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    # 'applicationinsights.django.ApplicationInsightsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR, 'client/dist')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'libraries': {
                'analytics': 'server.templatetags.analytics',
                'utils_templating': 'authentification.templatetags.utils_templating',
            },
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    path.join(BASE_DIR, 'client/dist/static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WSGI_APPLICATION = 'app.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.azuread_tenant.AzureADTenantOAuth2',
    'social_core.backends.okta.OktaOAuth2',
    'social_core.backends.okta_openidconnect.OktaOpenIdConnect',
    'django.contrib.auth.backends.ModelBackend',
]

HEADER_AUTH_USER_NAME = env('HEADER_AUTH_USER_NAME', '')
HEADER_AUTH_USER_GROUPS = env('HEADER_AUTH_USER_GROUPS', '')
HEADER_AUTH_ADMIN_GROUP_NAME = env('HEADER_AUTH_ADMIN_GROUP_NAME', '')
HEADER_AUTH_GROUPS_SEPERATOR = env('HEADER_AUTH_GROUPS_SEPERATOR', default=',')

if HEADER_AUTH_USER_NAME and HEADER_AUTH_USER_GROUPS and HEADER_AUTH_ADMIN_GROUP_NAME:
    MIDDLEWARE.append('server.middleware.HeaderAuthMiddleware')
    AUTHENTICATION_BACKENDS.append('django.contrib.auth.backends.RemoteUserBackend')

SOCIAL_AUTH_GITHUB_KEY = env('OAUTH_GITHUB_KEY', None)
SOCIAL_AUTH_GITHUB_SECRET = env('OAUTH_GITHUB_SECRET', None)
GITHUB_ADMIN_ORG_NAME = env('GITHUB_ADMIN_ORG_NAME', None)
GITHUB_ADMIN_TEAM_NAME = env('GITHUB_ADMIN_TEAM_NAME', None)

if GITHUB_ADMIN_ORG_NAME and GITHUB_ADMIN_TEAM_NAME:
    SOCIAL_AUTH_GITHUB_SCOPE = ['read:org']

SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = env('OAUTH_AAD_KEY', None)
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = env('OAUTH_AAD_SECRET', None)
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = env('OAUTH_AAD_TENANT', None)
AZUREAD_ADMIN_GROUP_ID = env('AZUREAD_ADMIN_GROUP_ID', None)

if AZUREAD_ADMIN_GROUP_ID:
    SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_RESOURCE = 'https://graph.microsoft.com/'
    SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SCOPE = ['Directory.Read.All']

SOCIAL_AUTH_OKTA_OAUTH2_KEY = env('OAUTH_OKTA_OAUTH2_KEY', None)
SOCIAL_AUTH_OKTA_OAUTH2_SECRET = env('OAUTH_OKTA_OAUTH2_SECRET', None)
SOCIAL_AUTH_OKTA_OAUTH2_API_URL = env('OAUTH_OKTA_OAUTH2_API_URL', None)
OKTA_OAUTH2_ADMIN_GROUP_NAME = env('OKTA_OAUTH2_ADMIN_GROUP_NAME', None)

if SOCIAL_AUTH_OKTA_OAUTH2_API_URL:
    SOCIAL_AUTH_OKTA_OAUTH2_SCOPE = ["groups"]

SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY = env('OAUTH_OKTA_OPENIDCONNECT_KEY', None)
SOCIAL_AUTH_OKTA_OPENIDCONNECT_SECRET = env('OAUTH_OKTA_OPENIDCONNECT_SECRET', None)
SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL = env('OAUTH_OKTA_OPENIDCONNECT_API_URL', None)
OKTA_OPENIDCONNECT_ADMIN_GROUP_NAME = env('OKTA_OPENIDCONNECT_ADMIN_GROUP_NAME', None)

if SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL:
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_SCOPE = ["groups"]

SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'server.social_auth.fetch_github_permissions',
    'server.social_auth.fetch_azuread_permissions',
    'server.social_auth.fetch_okta_oauth2_permissions',
    'server.social_auth.fetch_okta_openidconnect_permissions',
]

ROLE_PROJECT_ADMIN = env('ROLE_PROJECT_ADMIN', 'project_admin')
ROLE_ANNOTATOR = env('ROLE_ANNOTATOR', 'annotator')
ROLE_ANNOTATION_APPROVER = env('ROLE_ANNOTATION_APPROVER', 'annotation_approver')

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': env.int('DOCCANO_PAGE_SIZE', default=5),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'SEARCH_PARAM': 'q',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer'
    )
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_DIR = path.join(BASE_DIR, 'junitxml')

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/projects/'
LOGOUT_REDIRECT_URL = '/'

# dynamic import to avoid installing psycopg2 on pip installation.
name = 'django_heroku'
spec = importlib.util.find_spec(name)
if spec is not None:
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    module.settings(locals(), test_runner=False)

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(
    env='DATABASE_URL',
    conn_max_age=env.int('DATABASE_CONN_MAX_AGE', 500),
    ssl_require='sslmode' not in furl(env('DATABASE_URL', '')).args,
))

# work-around for dj-database-url: explicitly disable ssl for sqlite
if DATABASES['default'].get('ENGINE') == 'django.db.backends.sqlite3':
    DATABASES['default'].get('OPTIONS', {}).pop('sslmode', None)

# work-around for dj-database-url: patch ssl for mysql
if DATABASES['default'].get('ENGINE') == 'django.db.backends.mysql':
    DATABASES['default'].get('OPTIONS', {}).pop('sslmode', None)
    if env('MYSQL_SSL_CA', None):
        DATABASES['default'].setdefault('OPTIONS', {})\
            .setdefault('ssl', {}).setdefault('ca', env('MYSQL_SSL_CA', None))

# default to a sensible modern driver for Azure SQL
if DATABASES['default'].get('ENGINE') == 'sql_server.pyodbc':
    DATABASES['default'].setdefault('OPTIONS', {})\
        .setdefault('driver', 'ODBC Driver 17 for SQL Server')

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', False)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', False)
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', [])

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Size of the batch for creating documents
# on the import phase
IMPORT_BATCH_SIZE = env.int('IMPORT_BATCH_SIZE', 500)

GOOGLE_TRACKING_ID = env('GOOGLE_TRACKING_ID', 'UA-125643874-2').strip()

AZURE_APPINSIGHTS_IKEY = env('AZURE_APPINSIGHTS_IKEY', None)
APPLICATION_INSIGHTS = {
    'ikey': AZURE_APPINSIGHTS_IKEY if AZURE_APPINSIGHTS_IKEY else None,
    'endpoint': env('AZURE_APPINSIGHTS_ENDPOINT', None),
}

# necessary for email verification of new accounts
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', False)
EMAIL_HOST = env('EMAIL_HOST', None)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', None)
EMAIL_PORT = env.int('EMAIL_PORT', 587)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', 'webmaster@localhost')

if not EMAIL_HOST:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


if DEBUG:
    CORS_ORIGIN_WHITELIST = (
        'http://127.0.0.1:3000',
        'http://0.0.0.0:3000',
        'http://localhost:3000'
    )
