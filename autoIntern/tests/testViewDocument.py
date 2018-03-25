"""Tests the viewDocument function on the website"""
from autoIntern.models import User, Document
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase
from autoIntern.forms import UserForm

class ViewDocumentTest(TestCase):
    def setUp(self):
        user = User(email='test@test.com',
                    displayName='test',
                    firstName='test',
                    lastName='test',
                    group='test',
                    password='test',
                    title='test')
        user.save()
        content = b'10-K Report'
        doc = Document(company = 'APPLE_INC', doc_type = '10-K',
                       doc_date = '20171103',
                       doc_id = 'APPLE_INC.10-K.20171103', upload_id = user,
                       file = default_storage.save('static/document_folder/testing_file.txt',
                                                   ContentFile(content)))

        doc.save()


    def test_check_doc_loads_properly_login(self):
        response = self.client.post("/login/", {
            'email' : 'test@test.com',
            'password' : 'test'
        })
        self.assertTrue('APPLE_INC.10-K.20171103' in str(response.content))


    def test_check_doc_loads_properly_register(self):
        response = self.client.post("/register/", {
            'email' : 'test2@test.com',
            'displayName': 'test2',
            'firstName': 'test',
            'lastName': 'test',
            'group': 'test',
            'password': 'test2',
            'title': 'test2'
        })
        self.assertTrue('APPLE_INC.10-K.20171103' in str(response.content))


    def test_view_document_page(self):
        response = self.client.post("/login/", {
            'email' : 'test@test.com',
            'password' : 'test'
        })
        # Go to document
        response = self.client.get("/viewDocument?id=APPLE_INC.10-K.20171103")
        self.assertTrue('10-K Report' in str(response.content))


    def test_no_user_logged_in(self):
        response = self.client.get("/viewDocument?id=APPLE_INC.10-K.20171103")
        self.assertFalse('10-K Report' in str(response.content))
        self.assertTrue("/" == response.url)
