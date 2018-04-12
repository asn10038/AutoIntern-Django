from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [url(r'^', include('autoIntern.urls')),
               url(r'^admin/', admin.site.urls)]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
