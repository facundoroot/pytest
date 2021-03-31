from django.urls import reverse
import json
import pytest
from companies.models import Company
import logging

companies_url = reverse('companies-list')
# pytestmark es una forma de crear un mark que se aplica en todas las funciones, en este caso la que crea la db
pytestmark = pytest.mark.django_db


# ---------TestGetCompanies----------- #


def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_companie_exists_should_succeed(client) -> None:
    test_company = Company.objects.create(name='Amazon')
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get('name') == test_company.name
    assert response_content.get('status') == 'Hiring'
    assert response_content.get('application_link') == ''
    assert response_content.get('notes') == ''

# ---------TestPostCompanies----------- #


def test_create_companie_without_an_argument_should_fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {'name': ['This field is required.']}


def test_create_existing_company_should_fail(client) -> None:
    test_company = Company.objects.create(name='Google')
    response = client.post(companies_url, data={"name": "Google"})
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["company with this name already exists."]}


def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(
        companies_url, data={"name": "Test company name"}
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get('name') == 'Test company name'
    assert response_content.get('status') == 'Hiring'
    assert response_content.get('application_link') == ''
    assert response_content.get('notes') == ''


def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    response = client.post(
        companies_url, data={"name": "Test company name", "status": "Layoffs"}
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get('status') == 'Layoffs'


def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(
        companies_url, data={"name": "Test company name", "status": "WrongStatus"}
    )
    assert response.status_code == 400
    assert "WrongStatus" in str(response.content)
    assert "is not a valid choice" in str(response.content)


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