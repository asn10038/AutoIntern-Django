# creating test for storage of data

from autoIntern.models import Document
from autoIntern.models import User
from autoIntern.forms import UserForm
from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File
import os
from django.conf import settings


class DocumentModelTest(TestCase):
    def setUp(self):
        form = UserForm({
            'username': 'Test',
            'email' : 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test'
        })
        if form.is_valid():
            form.save()
        user = User.objects.get(username="Test")
        content = b'10-K Report'
        doc = Document(company = 'APPLE_INC', doc_type = '10-K',
                       doc_date = '20171103',
                       doc_id = 'APPLE_INC.10-K.20171103', upload_id = user,
                       file = default_storage.save('static/document_folder/testing_file.txt',
                                                   ContentFile(content)))

        doc.save()


    def test_file(self):
        doc = Document.objects.get(doc_id= 'APPLE_INC.10-K.20171103')
        content = doc.file.read()
        self.assertEquals(content, b'10-K Report')


    def test_labels(self):
        doc = Document.objects.get(doc_id='APPLE_INC.10-K.20171103')
        field_label = doc._meta.get_field('file').verbose_name
        self.assertEqual(field_label, 'file')

    def test_defstor(self):
        content = "<class 'storages.backends.gcloud.GoogleCloudStorage'>"
        self.assertEqual(str(default_storage.__class__) , content )

    def test_document_save(self):
        doc = Document.objects.get(doc_id='APPLE_INC.10-K.20171103')
        content = str(doc.file.url).replace("%2F", "/")
        self.assertEquals(content, 'https://storage.googleapis.com/autointern-dev/static/document_folder/testing_file.txt')
