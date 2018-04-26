from django.test import TestCase
from django.test import Client

def test_css(self):
    client = Client()
    response = client.get('/static/autoInternBase.css')
    assert (".mobileDropdown" in str(response.content))


def test_js(self):
    client = Client()
    response = client.get('/static/autoInternBase.js')
    assert ("highlightTags(tags)" in str(response.content))
