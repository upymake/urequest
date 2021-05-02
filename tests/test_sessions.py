from http import HTTPStatus

import _pytest
import pytest

from tests.mock.employees import Mock
from urequest import HttpUrl, Response, Session

pytestmark: _pytest.mark.MarkDecorator = pytest.mark.unittest


@pytest.fixture()
def _clean_up_employees(employees_mock: Mock) -> None:
    """Cleans up employees storage at teardown."""
    yield
    employees_mock.clean_up()


@pytest.mark.usefixtures("_clean_up_employees")
def test_session_get(employees_mock: Mock, session: Session) -> None:
    response: Response = session.get(HttpUrl(employees_mock.bind))
    assert response.is_ok()
    assert response.status() is HTTPStatus.OK
    assert str(response) == "Welcome to the employees test app!"


@pytest.mark.usefixtures("_clean_up_employees")
def test_session_post(employees_mock: Mock, session: Session) -> None:
    first_user_data = {"name": "Mike", "email": "mike@email.com"}
    first_user_response: Response = session.post(
        HttpUrl(employees_mock.bind, path="create_user"),
        as_dict=first_user_data,
    )
    assert first_user_response.is_ok()
    assert first_user_response.status() is HTTPStatus.CREATED
    assert first_user_response.as_json() == {**first_user_data, "id": 0}

    second_user_data = {"name": "Luke", "email": "luke@email.com"}
    second_user_response: Response = session.post(
        HttpUrl(employees_mock.bind, path="create_user"),
        as_dict=second_user_data,
    )
    assert second_user_response.is_ok()
    assert second_user_response.status() is HTTPStatus.CREATED
    assert second_user_response.as_json() == {**second_user_data, "id": 1}


@pytest.mark.usefixtures("_clean_up_employees")
def test_session_put(employees_mock: Mock, session: Session) -> None:
    create_response: Response = session.post(
        HttpUrl(employees_mock.bind, path="create_user"),
        as_dict={"name": "Mike", "email": "mike@email.com"},
    )
    user_id = create_response.as_json()["id"]
    update_response: Response = session.put(
        HttpUrl(employees_mock.bind, path=f"users/{user_id}"),
        as_dict={"name": "Mike", "email": "fake@email.com"},
    )
    assert update_response.is_ok()
    assert update_response.status() is HTTPStatus.OK
    assert update_response.as_json() == {
        "name": "Mike",
        "email": "fake@email.com",
        "id": user_id,
    }


@pytest.mark.usefixtures("_clean_up_employees")
def test_session_delete(employees_mock: Mock, session: Session) -> None:
    data = {"name": "Mike", "email": "mike@email.com"}
    create_user_response: Response = session.post(
        HttpUrl(employees_mock.bind, path="create_user"), as_dict=data
    )
    users_response: Response = session.get(
        HttpUrl(employees_mock.bind, path="users")
    )
    user_id = create_user_response.as_json()["id"]
    assert users_response.is_ok()
    assert users_response.status() is HTTPStatus.OK
    assert users_response.as_json() == [{**data, "id": user_id}]
    delete_user_response: Response = session.delete(
        HttpUrl(employees_mock.bind, path=f"users/{user_id}")
    )
    assert delete_user_response.is_ok()
    assert delete_user_response.status() is HTTPStatus.NO_CONTENT
    users_response: Response = session.get(
        HttpUrl(employees_mock.bind, path="users")
    )
    assert users_response.is_ok()
    assert users_response.status() is HTTPStatus.OK
    assert users_response.as_json() == []
