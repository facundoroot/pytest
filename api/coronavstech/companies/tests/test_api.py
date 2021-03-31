from unittest import TestCase
from django.test import Client
from django.urls import reverse
import json
import pytest
from companies.models import Company
import logging


@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.companies_url = reverse('companies-list')

    def tearDown(self):
        pass


class TestGetCompanies(BasicCompanyAPITestCase):

    def test_zero_companies_should_return_empty_list(self) -> None:
        #llamo a la lista y aparte le agrego el -list que hace que el request sea un get
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_companie_exists_should_succeed(self) -> None:
        test_company = Company.objects.create(name='Amazon')
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get('name'), test_company.name)
        self.assertEqual(response_content.get('status'), 'Hiring')
        self.assertEqual(response_content.get('application_link'), '')
        self.assertEqual(response_content.get('notes'), '')


class TestPostCOmpanies(BasicCompanyAPITestCase):
    def test_create_companie_without_an_argument_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {'name': ['This field is required.']}
        )

    def test_create_existing_company_should_fail(self) -> None:
        test_company = Company.objects.create(name='Google')
        response = self.client.post(self.companies_url, data={"name": "Google"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), 
            {"name": ["company with this name already exists."]}
        )

    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(
            self.companies_url, data={"name": "Test company name"}
        )
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get('name'), 'Test company name')
        self.assertEqual(response_content.get('status'), 'Hiring')
        self.assertEqual(response_content.get('application_link'), '')
        self.assertEqual(response_content.get('notes'), '')

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:
        response = self.client.post(
            self.companies_url, data={"name": "Test company name", "status": "Layoffs"}
        )
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get('status'), 'Layoffs')

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:
        response = self.client.post(
            self.companies_url, data={"name": "Test company name", "status": "WrongStatus"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("WrongStatus", str(response.content))
        self.assertIn("is not a valid choice", str(response.content))

    @pytest.mark.xfail
    def test_should_be_ok_if_fails(self) -> None:
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_should_be_skipped(self) -> None:
        self.assertEqual(1, 2)

#Comienza Pytest

@pytest.mark.xfail
def test_should_be_ok_if_fails(self) -> None:
    assert 1 == 2

@pytest.mark.skip
def test_should_be_skipped(self) -> None:
    assert 1 == 2


# creo una excepcion
def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")


# atajo la excepcion
def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)

# guardo un log
logger = logging.getLogger('CORONA LOGS')


def function_that_logs_something() -> None:
    try:
        raise ValueError('CoronaVirus Exception')
    except ValueError as e:
        logger.warning(f'I am logging {str(e)}')

def test_logged_warning_level(caplog) -> None:
    function_that_logs_something()
    assert 'I am logging CoronaVirus Exception' in caplog.text