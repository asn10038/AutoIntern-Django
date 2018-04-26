"""Tests the forms on the website"""
from autoIntern.models import User
from django.test import TestCase
from autoIntern.forms import UserForm

class RegisterFormTest(TestCase):
    def setUp(self):
        pass

    def test_valid_data(self):
        form = UserForm({
            'username': 'Test',
            'email' : 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = UserForm({
            'username': 'Test',
            'email' : 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test'
        })
        self.assertFalse(form.is_valid())

    def test_home_view(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'autoIntern/homePage.html')

    def test_register_user_form_view(self):
        user_count = User.objects.count()
        response = self.client.post("/register/", {
            'username': 'Test',
            'email' : 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test'
        })
        self.assertEqual(User.objects.count(), user_count + 1)

    def test_user_login_view(self):
        form = UserForm({
            'username': 'Test',
            'email' : 'test@test.com',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test'
        })
        if form.is_valid():
            form.save()
        self.assertIsNotNone(User.objects.get(email='test@test.com'))

        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })
        response = self.client.get("/")
        self.assertTrue('Hello' in str(response.content))

    def test_logout(self):
        response = self.client.post("/userLogin/", {
            'username': 'Test',
            'password': 'test'
        })
        response = self.client.post("/userLogout/")

        self.assertFalse('Hello' in str(response.content))
