from autoIntern.models import Document
from autoIntern.models import User
from autoIntern.forms import UserForm
from autoIntern.models import Case
from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File
import os
from django.conf import settings
from autoIntern.helpers import get_docs_in_case


class CaseModelTest(TestCase):
    def setUp(self):
        form = UserForm({
            'username': 'Test',
            'email': 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test'
        })
        if form.is_valid():
            form.save()
        user = User.objects.get(username="Test")
        content = b'10-K Report'
        doc = Document(company='APPLE_INC', doc_type='10-K',
                       doc_date='20171103',
                       doc_id='APPLE_INC.10-K.20171103', upload_id=user,
                       file=default_storage.save('static/document_folder/testing_file.txt',
                                                   ContentFile(content)))

        doc.save()

        case = Case(case_name='Case Test')
        case.save()
        doc1 = Document.objects.get(doc_id='APPLE_INC.10-K.20171103')
        case.documents.add(doc1)
        case.user_permissions.add(user)

        # Adding user without permissions
        form2 = UserForm({
            'username': 'Test2',
            'email': 'test2@test.com',
            'first_name': 'test2',
            'last_name': 'test2',
            'password': 'test2'
        })
        if form2.is_valid():
            form2.save()

    def test_doc_in_case(self):
        case = Case.objects.get(case_name='Case Test')
        docs = get_docs_in_case(case.case_id)
        self.assertEquals(docs[0].doc_id, 'APPLE_INC.10-K.20171103')

    def test_users_in_case(self):
        case = Case.objects.get(case_name='Case Test')
        users = case.user_permissions.all()[0]
        tester = User.objects.get(username='Test')
        self.assertEquals(users, tester)

    def test_unauthorized_user(self):
        response = self.client.post("/userLogin/", {
            'username': 'Tes2',
            'password': 'test2'
        })
        case = Case.objects.get(case_name='Case Test')
        response = self.client.get("/viewCase", {
            'id': str(case.case_id)
        })
        self.assertFalse('Hello' in str(response.content))

    def test_get_error(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })
        response = self.client.get("/viewCase", {
            'id': 'INVALID ID'
        })
        self.assertTrue("/error" == response.url)