import os

from django.core.wsgi import get_wsgi_application

SETTINGS = "mysite.settings.base"
try:
    if os.environ["ENVIRONMENT"] == 'UAT':
        SETTINGS = "mysite.settings.uat"
    if os.environ["ENVIRONMENT"] == 'PROD':
        SETTINGS = "mysite.settings.prod"
except KeyError as ke:
    pass
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS)

application = get_wsgi_application()
