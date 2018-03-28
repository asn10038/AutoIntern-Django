import os
import sys
from django.conf import settings
from django.core.files.storage import default_storage
from google.cloud import storage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
# FIX ASAP
SECRET_KEY = 'pf-@jxtojga)z+4s*uwbgjrq$aep62-thd0q7f&o77xtpka!_m'

#

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'autoIntern',
    'bootstrap4',
    'widget_tweaks',
    'storages',
    'google.cloud.storage'
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/DjangoDebug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# [START dbconfig]
if os.getenv('GAE_INSTANCE'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': '024lana',
            'PORT': '5432',
            'HOST': '/cloudsql/autointern-dev:us-east1:autointern-dev',
        },
    }
elif os.getenv('SETTINGS_MODE') == 'prod':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'supersecret',
            'PORT': '5432',
            'HOST': '127.0.0.1',
            'INSTANCE': '104.196.145.166'
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': '024lana',
            'PORT': '5432',
            'HOST': '127.0.0.1',
            'INSTANCE': '35.185.112.154'

        },
    }
# [END dbconfig]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'EST'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# [START staticurl]
STATIC_URL = 'https://storage.googleapis.com/autointern-dev/static/'
STATIC_ROOT = 'static/'
# [END staticurl]




try:
    from google.cloud.storage.client import Client
    from google.cloud.storage.blob import Blob
    from google.cloud.exceptions import NotFound
except ImportError:
    raise ImproperlyConfigured("Could not load Google Cloud Storage bindings.\n"
                               "See https://github.com/GoogleCloudPlatform/gcloud-python")



# Google Cloud Static Settings
# [START Gcloud Static]
######################
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'autointern-dev'  # /static/document_folder'
GS_PROJECT_ID = 'autointern-dev'


####
# project_id = setting('GS_PROJECT_ID', None)
# credentials = setting('GS_CREDENTIALS', None)
# setting('GS_BUCKET_NAME', None)
# location = setting('GS_LOCATION', '')
# auto_create_bucket = setting('GS_AUTO_CREATE_BUCKET', False)
# auto_create_acl = setting('GS_AUTO_CREATE_ACL', 'projectPrivate')
# file_name_charset = setting('GS_FILE_NAME_CHARSET', 'utf-8')
# file_overwrite = setting('GS_FILE_OVERWRITE', True)
# max_memory_size = setting('GS_MAX_MEMORY_SIZE', 0)
######

#  [END Gcloud Static]



# Local file storage setting
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


#### media root fix ???

# MEDIA_ROOT = os.path.join(DEFAULT_FILE_STORAGE, '/document_folder/')
