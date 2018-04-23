"""Functionality on the Admin Page"""
from django.contrib import admin
from autoIntern import models

admin.site.register(models.Document)
admin.site.register(models.Case)
admin.site.register(models.Data)
admin.site.register(models.Permissions)
