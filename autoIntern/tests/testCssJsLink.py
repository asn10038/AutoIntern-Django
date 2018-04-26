from django.test import TestCase
from django.test import Client

def testIndex(self):
    client = Client()
    response = client.get('/static/autoInternBase.css')
    assert (".mobileDropdown" in str(response.content))


def testIndex(self):
    client = Client()
    response = client.get('/static/autoInternBase.js')
    assert ("highlightTags(tags)" in str(response.content))
