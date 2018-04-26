from autoIntern.models import Document
from autoIntern.models import User
from autoIntern.forms import UserForm
from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage




class NoteUploadTest(TestCase):
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
        content = b'This is a test note'
        note_name = 'new_note_name'
        doc = Document(company=note_name, doc_type='note',
                       doc_date='20171103',
                       doc_id='testing_note.txt', upload_id=user,
                       file=default_storage.save('static/document_folder/testing_note.txt',
                                                 ContentFile(content)))

        doc.save()


    def test_note(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })
        doc = Document.objects.get(doc_id='testing_note.txt')
        content = doc.file.read()
        self.assertEquals(content, b'This is a test note')


    def test_note_save(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })
        doc = Document.objects.get(company='new_note_name')
        content = str(doc.file.url).replace("%2F", "/")
        self.assertEquals(content, 'https://storage.googleapis.com/autointern-dev/static/document_folder/testing_note.txt')