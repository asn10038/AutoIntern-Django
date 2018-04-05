# creating test for storage of documents and data in cases

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
from autoIntern.views.views import get_docs_in_case


class CaseModelTest(TestCase):
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

        case = Case( case_name = 'Case Test')
        case.save()
        doc1 = Document.objects.get(doc_id = 'APPLE_INC.10-K.20171103')
        case.documents.add(doc1)
        case.user_permissions.add(user)

    def test_doc_in_case(self):
        case = Case.objects.get(case_name = 'Case Test')
        docs = get_docs_in_case( case.case_id)
        self.assertEquals( docs[0].doc_id,'APPLE_INC.10-K.20171103' )

    def test_users_in_case(self):
        case = Case.objects.get(case_name = 'Case Test')
        users = case.user_permissions.all()[0]
        tester = User.objects.get(username='Test')
        self.assertEquals(users, tester )
