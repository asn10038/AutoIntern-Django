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
        Manager = User.objects.get(username="Manager")

        form = UserForm({
            'username': 'BaseUser',
            'email': 'BaseUser@test.com',
            'first_name': 'BaseUser',
            'last_name': 'BaseUser',
            'password': 'BaseUser'
        })
        if form.is_valid():
            form.save()
        BaseUser = User.objects.get(username="BaseUser")

        form = UserForm({
            'username': 'Test1',
            'email': 'test1@test.com',
            'first_name': 'test1',
            'last_name': 'test1',
            'password': 'test1'
        })
        if form.is_valid():
            form.save()
        user1 = User.objects.get(username="Test1")

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


        case = Case(case_name='Case Test', case_id=999999)
        case.save()

        managerPerm = Permissions(case=case, user=Manager, user_type=Permissions.MANAGER_USER)
        managerPerm.save()

        userPerm = Permissions(case=case, user=BaseUser, user_type=Permissions.BASE_USER)
        userPerm.save()


    def testAddRemoveUsers(self):
        response = self.client.post("/userLogin/", {
            'username': 'Manager',
            'password': 'Manager'
        })

        case = Case.objects.get(case_id=999999)
        user1 = User.objects.get(username="Test1")
        user2 = User.objects.get(username="Test2")

        response = self.client.post('/addUsers/', {
            'case_id': str(case.case_id),
            'ids[]': (str(user1.username), str(user2.username)),
        })

        self.assertTrue(Permissions.objects.filter(case=case, user=user1).exists())
        self.assertTrue(Permissions.objects.filter(case=case, user=user2).exists())

        perm1 = Permissions.objects.all().get(case=case, user=user1)
        perm2 = Permissions.objects.all().get(case=case, user=user2)


        # Testing users properly added
        self.assertTrue(user1 in case.user_permissions.all())
        self.assertTrue(perm1.user_type == Permissions.BASE_USER)

        self.assertTrue(user2 in case.user_permissions.all())
        self.assertTrue(perm2.user_type == Permissions.BASE_USER)

        response = self.client.post('/removeUsers/', {
            'case_id': str(case.case_id),
            'ids[]': (str(user1.username), str(user2.username)),
        })

        # Testing users properly removed
        self.assertFalse(user1 in case.user_permissions.all())
        self.assertFalse(user2 in case.user_permissions.all())

        self.assertTrue(Permissions.objects.all().filter(case=case, user=user1).count() == 0)
        self.assertTrue(Permissions.objects.all().filter(case=case, user=user2).count() == 0)


    def testAddInvalidCase(self):
        response = self.client.post("/userLogin/", {
            'username': 'Manager',
            'password': 'Manager'
        })

        user1 = User.objects.get(username="Test1")
        user2 = User.objects.get(username="Test2")

        response = self.client.post('/addUsers/', {
            'case_id': 'INVALID',
            'ids[]': (str(user1.username), str(user2.username)),
        })

        self.assertTrue("/" == response.url)


    def testRemoveInvalidCase(self):
        response = self.client.post("/userLogin/", {
            'username': 'Manager',
            'password': 'Manager'
        })

        user1 = User.objects.get(username="Test1")
        user2 = User.objects.get(username="Test2")

        response = self.client.post('/removeUsers/', {
            'case_id': 'INVALID',
            'ids[]': (str(user1.username), str(user2.username)),
        })

        self.assertTrue("/" == response.url)


    def testUserAttemptsAdd(self):
        response = self.client.post("/userLogin/", {
            'username': 'BaseUser',
            'password': 'BaseUser'
        })

        case = Case.objects.get(case_id=999999)
        user1 = User.objects.get(username="Test1")
        user2 = User.objects.get(username="Test2")

        response = self.client.post('/addUsers/', {
            'case_id': str(case.case_id),
            'ids[]': (str(user1.username), str(user2.username)),
        })

        self.assertTrue("/" == response.url)


    def testUserAttemptsRemove(self):
        response = self.client.post("/userLogin/", {
            'username': 'BaseUser',
            'password': 'BaseUser'
        })

        case = Case.objects.get(case_id=999999)
        user1 = User.objects.get(username="Test1")
        user2 = User.objects.get(username="Test2")

        response = self.client.post('/removeUsers/', {
            'case_id': str(case.case_id),
            'ids[]': (str(user1.username), str(user2.username)),
        })

        self.assertTrue("/" == response.url)