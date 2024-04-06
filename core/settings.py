import os
from pathlib import Path
from django.contrib.messages import constants as messages
import json
import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

# ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure-rr@o^o5z%#mb^dtjtlbbc^4yuhlbkujnjeeskhczwf($=6d_0i"

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = env.list('ALLOWED_HOST_DEV')


# Application definition

DJANGO_APPS  = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    'apps.authentication',
    'apps.home',
    'apps.contact',
    'apps.request',
    'apps.client_management',

]


THIRD_PARTY_APPS = [
    # 'corsheaders',
    #'rest_framework',
    'ckeditor',
    # 'ckeditor_uploader',
    'livereload',
    'six',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

HANDLER404 = 'apps.Error_Handler.views.Error404View'
HANDLER500 = 'apps.Error_Handler.views.Error505View'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'autoParagraph': False
    }
}

CKEDITOR_UPLOAD_PATH = "/media/"

SESSION_SAVE_EVERY_REQUEST = True

with open('language.json', 'r', encoding='utf-8') as file:
    LANGUAGE_DATA = json.load(file)

    
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',
    'core.languagemiddleware.LanguageMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/ 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}




AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

DATE_INPUT_FORMATS =  ['%d-%m-%Y']

USE_I18N = True

USE_TZ = True



STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'core/static')
# ]

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATIC_URL = '/assets/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/assets')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'django_gcp/staticfiles/dash/component/dash_bootstrap_components/_components/dash_bootstrap_components.min.js')

PLOTLY_DASH = {

    # Route used for the message pipe websocket connection
    "ws_route" :   "dpd/ws/channel",

    # Route used for direct http insertion of pipe messages
    "http_route" : "dpd/views",

    # Flag controlling existince of http poke endpoint
    "http_poke_enabled" : True,

    # Insert data for the demo when migrating
    "insert_demo_migrations" : False,

    # Timeout for caching of initial arguments in seconds
    "cache_timeout_initial_arguments": 60,

    # Name of view wrapping function
    "view_decorator": None,

    # Flag to control location of initial argument storage
    "cache_arguments": True,

    # Flag controlling local serving of assets
    "serve_locally": False,
    # Name of view wrapping function
    "view_decorator": "django_plotly_dash.access.login_required",
}

PLOTLY_COMPONENTS = [
    # core components required for use of most plotly dash components
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',
    'dash_bootstrap_components',
    # django-plotly-dash components
    'dpd_components',
    'dpd_static_support',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}


DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # Aumenta el límite a 5MB


# email stuff
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.Emailbackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field



X_FRAME_OPTIONS = 'SAMEORIGIN'
CSRF_COOKIE_NAME = 'csrftoken'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'welcome'


AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'backendspglobal'
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'



# if not DEBUG:
#     ALLOWED_HOST=env.list('ALLOWED_HOST_DEPLOY')
