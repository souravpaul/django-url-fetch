from django.test import TestCase
from .models import CheckURL

# Create your tests here.

class CheckURLCase(TestCase):
    def setUp(self):
        CheckURL.objects.create(url="https://google.com", status_code="200",comment="OK",key="123")
        CheckURL.objects.create(url="https://facebook.com", status_code="200",comment="OK",key="123")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        google = CheckURL.objects.get(url="https://google.com",key="123")
        fecebook = CheckURL.objects.get(url="https://facebook.com",key="123")