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


class CreateCaseTest(TestCase):
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

        case = Case(case_name='Case Test')
        case.save()

    def test_new_create_case(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })

        response = self.client.post('/createCase/', {
            'caseName': 'New Case Test',
        })

        case = Case.objects.all().filter(case_name='New Case Test')
        self.assertTrue(case.count() > 0)

    def test_existing_create_case(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })

        response = self.client.post('/createCase/', {
            'caseName': 'Case Test',
        })

        case = Case.objects.all().filter(case_name='Case Test(1)')
        self.assertTrue(case.count() > 0)
