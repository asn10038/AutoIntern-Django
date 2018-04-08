from autoIntern.models import User, Document
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase
from autoIntern.forms import UserForm

class CreateTagTest(TestCase):
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

    def test_createTag(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })
        response = self.client.post('/createTag/', {
            'path': '/viewDocument?id=APPLE_INC.10-K.20171103',
            'currentDocumentId' : 'APPLE_INC.10-K.20171103',
            'newTagLabel' : 'testLabel',
            'newTagContent' : 'testValue',
            'newTagLineNum' : '4',
            'newTagIndex' : '24'
        })
