from unittest import TestCase
from django.test import Client
from django.urls import reverse
import json
import pytest

@pytest.mark.django_db
class TestGetCompanies(TestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        client = Client()
        #llamo a la lista y aparte le agrego el -list que hace que el request sea un get
        companies_url = reverse('companies-list')
        response = client.get(companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])
