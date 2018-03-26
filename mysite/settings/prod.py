from mysite.settings.base import *


DEBUG = False

# Database
# [START dbconfig]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'supersecret',
        'PORT': '5432',
        'HOST': '/cloudsql/autointern-prod:us-east1:autointern-prod'
    },
}
# [END dbconfig]


# Static files (CSS, JavaScript, Images)
# [START staticurl]
GS_BUCKET_NAME = 'autointern-prod'
GS_PROJECT_ID = 'autointern-prod'
STATIC_URL = 'https://storage.googleapis.com/autointern-prod/static/'
STATIC_ROOT = 'static/'
# [END staticurl]
