from django.test import TestCase
from django.test import Client

class ViewsTestCase(TestCase):
    def testIndex(self):
        client = Client()
        response = client.get('/')
        assert("AutoIntern" in str(response.content))