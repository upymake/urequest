import pytest

from tests.mock import Endpoint
from tests.mock.employees import EmployeesMock, Mock
from urequest.credentials import Credentials
from urequest.response import Response
from urequest.session import HttpSession, LoggedHttpSession, Session
from urequest.url import Address, HttpUrl


@pytest.fixture(scope="session")
def session_url() -> Address:
    return HttpUrl(host="xkcd.com", path="info.0.json")


@pytest.fixture(scope="session")
def credentials() -> Credentials:
    return Credentials(username="superuser", password="superpass")


@pytest.fixture(scope="session")
def session() -> Session:
    with HttpSession() as http_session:  # type: Session
        return http_session


@pytest.fixture(scope="session")
def logged_session(credentials: Credentials) -> Session:
    with LoggedHttpSession(
        credentials
    ) as logged_http_session:  # type: Session
        return logged_http_session


@pytest.fixture(scope="session")
def response(session: Session, session_url: Address) -> Response:
    return session.get(session_url)


@pytest.fixture(scope="session")
def logged_response(logged_session: Session, session_url: Address) -> Response:
    return logged_session.get(session_url)


@pytest.fixture(scope="session")
def employees_mock() -> Mock:
    with EmployeesMock(Endpoint(host="0.0.0.0", port=4444)) as mock:
        return mock
