from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class Document(models.Model):
    doc_id = models.CharField(max_length=255, primary_key=True)
    company = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=255)
    doc_date = models.CharField(max_length=255)
    upload_id = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_datetime = models.DateTimeField(auto_now_add=True, editable=True)
    file = models.FileField(upload_to='document_folder')

    def get_identifiers(self):
        header = str(self.file.read(), 'utf-8')
        header = header.split('\n')[:45]
        company = ''
        doc_type = ''
        doc_date = ''
        for line in header:
            split = line.split(':')
            if '<SEC-DOCUMENT>' in split[0]:
                doc_date = split[1].strip()
            if 'CONFORMED SUBMISSION TYPE' in split[0]:
                doc_type = split[1].strip()
            if 'COMPANY CONFORMED NAME' in split[0]:
                company = split[1].strip()
                company = company.replace(' ', '_')
        return (company, doc_type, doc_date)


class Case(models.Model):
    case_id = models.AutoField(primary_key=True)
    case_name = models.CharField(max_length=255, default= 'Base Case')
    create_datetime = models.DateTimeField(auto_now_add=True)
    documents = models.ManyToManyField(Document)
    user_permissions = models.ManyToManyField(User)


class Data(models.Model):
    data_id = models.AutoField(primary_key=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # case = models.ForeignKey(Case, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(auto_now_add=True)
    value = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    line = models.CharField(max_length=255)
    index = models.CharField(max_length=255)
    rangySelection = models.CharField(max_length=255) #serialized selection object from rangy plugin
    current = models.NullBooleanField(blank=True, null=True)

class Permissions(models.Model):
    BASE_USER = 1
    MANAGER_USER = 2
    USER_CHOICES = (
        (BASE_USER, 'Base'),
        (MANAGER_USER, 'Manager'),
    )

    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.IntegerField(choices=USER_CHOICES, default=BASE_USER)