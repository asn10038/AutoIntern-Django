"""Tests the exportTags function on the website"""
from autoIntern.models import User, Document
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase
from autoIntern.forms import UserForm

class ViewDocumentTest(TestCase):
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

    def test_invalid_access(self):
        response = self.client.get('/exportTags/')
        self.assertTrue("/" == response.url)

    def test_csv_output(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })
        response = self.client.post('/exportTags/', {
            'path': '/viewDocument?id=APPLE_INC.10-K.20171103',
            'csv': ''
        })
        output = response.serialize().decode("utf-8")

        self.assertTrue("charset=utf8" in output)
        self.assertTrue("Content-Disposition: attachment;" in output)
        self.assertTrue("Content-Type: text/csv;" in output)
        self.assertTrue("APPLE_INC" in output)
        self.assertTrue("10-K" in output)
        self.assertTrue("20171103" in output)

    def test_txt_output(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })
        response = self.client.post('/exportTags/', {
            'path': '/viewDocument?id=APPLE_INC.10-K.20171103',
            'txt': ''
        })

        output = response.serialize().decode("utf-8")

        self.assertTrue("charset=utf8" in output)
        self.assertTrue("Content-Disposition: attachment;" in output)
        self.assertTrue("Content-Type: text/plain;" in output)
        self.assertTrue("APPLE_INC" in output)
        self.assertTrue("10-K" in output)
        self.assertTrue("20171103" in output)

    def test_json_output(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })
        response = self.client.post('/exportTags/', {
            'path': '/viewDocument?id=APPLE_INC.10-K.20171103',
            'json': ''
        })

        output = response.serialize().decode("utf-8")

        self.assertTrue("charset=utf8" in output)
        self.assertTrue("Content-Disposition: attachment;" in output)
        self.assertTrue("Content-Type: application/javascript;" in output)
        self.assertTrue("APPLE_INC" in output)
        self.assertTrue("10-K" in output)
        self.assertTrue("20171103" in output)

    def test_invalid_doc_id_format(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })
        response = self.client.post('/exportTags/', {
            'path': 'INVALIDDOC',
            'txt': ''
        })
        self.assertTrue("/" == response.url)

    def test_nonexistent_doc(self):
        response = self.client.post("/login/", {
            'email': 'test@test.com',
            'password': 'test'
        })
        response = self.client.post('/exportTags/', {
            'path': '/viewDocument?id=NONEXISTENT-DOC',
            'txt': ''
        })
        self.assertTrue("/" == response.url)
