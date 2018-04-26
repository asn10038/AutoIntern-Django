"""Tests the exportTagsCase function on the website - exports tags across documents"""
from autoIntern.models import User, Document, Data
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase
from autoIntern.forms import UserForm

class ExportTagsAcrossCaseTest(TestCase):
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

        doc2 = Document(company='APPLE_INC', doc_type='10-K',
                       doc_date='20171104',
                       doc_id='APPLE_INC.10-K.20171104', upload_id=user,
                       file=default_storage.save('static/document_folder/testing_file.txt',
                                                 ContentFile(content)))
        doc2.save()


    def test_invalid_access(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })

        response = self.client.get('/exportTagsCase/')
        self.assertTrue("/" == response.url)

    def test_output(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })

        response = self.client.post('/createTag/', {
            'path': '/viewDocument?id=APPLE_INC.10-K.20171103',
            'currentDocumentId': 'APPLE_INC.10-K.20171103',
            'newTagLabel': 'label1',
            'newTagContent': 'value1',
            'newTagLineNum': '4',
            'newTagIndex': '24',
            'serializedRangySelection': '0/0/17/1/1/1/1/0/2/1/13/29/2:0,0/0/17/1/1/1/1/0/2/1/13/29/2:7'
        })

        response = self.client.post('/createTag/', {
            'path': '/viewDocument?id=APPLE_INC.10-K.20171103',
            'currentDocumentId': 'APPLE_INC.10-K.20171103',
            'newTagLabel': 'label2',
            'newTagContent': 'value2',
            'newTagLineNum': '5',
            'newTagIndex': '24',
            'serializedRangySelection': '0/0/17/1/1/1/1/0/2/1/13/29/2:0,0/0/17/1/1/1/1/0/2/1/13/29/2:7'
        })

        response = self.client.post('/createTag/', {
            'path': '/viewDocument?id=APPLE_INC.10-K.20171104',
            'currentDocumentId': 'APPLE_INC.10-K.20171104',
            'newTagLabel': 'label1',
            'newTagContent': 'value3',
            'newTagLineNum': '4',
            'newTagIndex': '24',
            'serializedRangySelection': '0/0/17/1/1/1/1/0/2/1/13/29/2:0,0/0/17/1/1/1/1/0/2/1/13/29/2:7'
        })

        response = self.client.post('/exportTagsCase/', {
            'doc_ids[]': ('APPLE_INC.10-K.20171103', 'APPLE_INC.10-K.20171104')
        })
        output = response.serialize().decode("utf-8")

        self.assertTrue("charset=utf8" in output)
        self.assertTrue("Content-Disposition: attachment;" in output)
        self.assertTrue("Content-Type: text/csv;" in output)
        self.assertTrue("APPLE_INC" in output)
        self.assertTrue("10-K" in output)
        self.assertTrue("20171103" in output)
        self.assertTrue("20171104" in output)
        self.assertTrue("label1" in output)
        self.assertTrue("value1" in output)
        self.assertTrue("value3" in output)
        self.assertTrue("label2" in output)
        self.assertTrue("value2" in output)

    def test_invalid_documents(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })
        response = self.client.post('/exportTagsCase/', {
            'doc_ids[]': (str('NONEXISTENT_DOC'),)
        })
        self.assertTrue("/error" == response.url)
