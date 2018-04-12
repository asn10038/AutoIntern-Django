"""Tests the addUsers function on the website"""
from autoIntern.models import User, Case, Permissions
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase
from autoIntern.forms import UserForm

class AddUsersTest(TestCase):
    def setUp(self):
        form = UserForm({
            'username': 'Manager',
            'email' : 'Manager@test.com',
            'first_name': 'Manager',
            'last_name': 'Manager',
            'password': 'Manager'
        })
        if form.is_valid():
            form.save()
        user = User.objects.get(username="Manager")

        form = UserForm({
            'username': 'Test2',
            'email': 'test2@test.com',
            'first_name': 'test2',
            'last_name': 'test2',
            'password': 'test2'
        })
        if form.is_valid():
            form.save()
        user2 = User.objects.get(username="Test2")

        form = UserForm({
            'username': 'Test3',
            'email': 'test3@test.com',
            'first_name': 'test3',
            'last_name': 'test3',
            'password': 'test3'
        })
        if form.is_valid():
            form.save()
        user3 = User.objects.get(username="Test3")

        form = UserForm({
            'username': 'Test4',
            'email': 'test4@test.com',
            'first_name': 'test4',
            'last_name': 'test4',
            'password': 'test4'
        })
        if form.is_valid():
            form.save()
        user4 = User.objects.get(username="Test4")

        case = Case(case_name='Case Test', case_id=999999)

        case.save()


    def testAddRemoveUsers(self):
        response = self.client.post("/userLogin/", {
            'username': 'Manager',
            'password': 'Manager'
        })

        case = Case.objects.get(case_id=999999)
        user2 = User.objects.get(username="Test2")
        user3 = User.objects.get(username="Test3")

        response = self.client.post('/addUsers/', {
            'case_id': str(case.case_id),
            'ids[]': (str(user2.username), str(user3.username)),
        })

        perm2 = Permissions.objects.all().get(case=case, user=user2)
        perm3 = Permissions.objects.all().get(case=case, user=user3)


        # Testing users properly added
        self.assertTrue(user2 in case.user_permissions.all())
        self.assertTrue(perm2.user_type == Permissions.BASE_USER)

        self.assertTrue(user3 in case.user_permissions.all())
        self.assertTrue(perm3.user_type == Permissions.BASE_USER)

        response = self.client.post('/removeUsers/', {
            'case_id': str(case.case_id),
            'ids[]': (str(user2.username), str(user3.username)),
        })


        # Testing users properly removed
        self.assertFalse(user2 in case.user_permissions.all())
        self.assertFalse(user3 in case.user_permissions.all())

        self.assertTrue(Permissions.objects.all().filter(case=case, user=user2).count() == 0)
        self.assertTrue(Permissions.objects.all().filter(case=case, user=user3).count() == 0)


    def testAddInvalidCase(self):
        response = self.client.post("/userLogin/", {
            'username': 'Manager',
            'password': 'Manager'
        })

        user2 = User.objects.get(username="Test2")
        user3 = User.objects.get(username="Test3")

        response = self.client.post('/addUsers/', {
            'case_id': 'INVALID',
            'ids[]': (str(user2.username), str(user3.username)),
        })

        self.assertTrue("/" == response.url)


    def testRemoveInvalidCase(self):
        response = self.client.post("/userLogin/", {
            'username': 'Manager',
            'password': 'Manager'
        })

        user2 = User.objects.get(username="Test2")
        user3 = User.objects.get(username="Test3")

        response = self.client.post('/removeUsers/', {
            'case_id': 'INVALID',
            'ids[]': (str(user2.username), str(user3.username)),
        })

        self.assertTrue("/" == response.url)


    def testRemoveUserNotInCase(self):
        response = self.client.post("/userLogin/", {
            'username': 'Manager',
            'password': 'Manager'
        })

        case = Case.objects.get(case_id=999999)
        user4 = User.objects.get(username="Test4")

        response = self.client.post('/removeUsers/', {
            'case_id': str(case.case_id),
            'ids[]': (str(user4.username),),
        })

        self.assertTrue("/" == response.url)