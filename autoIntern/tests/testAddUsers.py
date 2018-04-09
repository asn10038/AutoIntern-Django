"""Tests the addUsers function on the website"""
from autoIntern.models import User, Case, Permissions
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase
from autoIntern.forms import UserForm

class AddUsersTest(TestCase):
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

        case = Case(case_name='Case Test', case_id=999)
        #case.user_permissions.add(user)
        #case.save()

    def testAddUsers(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })

        case = Case.objects.filter(case_name='Case Test')
        user = User.objects.get(username="Test")

        response = self.client.post('/addUsers/', {
            'case_id': str(case.case_id),
            'ids[]': '[Test]'
        })