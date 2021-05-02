import pytest

from tests.mock.users import UsersMock
from urequest.credentials import Credentials
from urequest.response import Response
from urequest.session import HttpSession, LoggedHttpSession, Session
from urequest.url import Address, HttpUrl


@pytest.fixture(scope="session")
def session_url() -> Address:
    return HttpUrl(host="xkcd.com", path="info.0.json")


@pytest.fixture(scope="session")
def credentials() -> Credentials:
    yield Credentials(username="superuser", password="superpass")


@pytest.fixture(scope="session")
def session() -> Session:
    with HttpSession() as http_session:  # type: Session
        yield http_session


@pytest.fixture(scope="session")
def logged_session(credentials: Credentials) -> Session:
    with LoggedHttpSession(
        credentials
    ) as logged_http_session:  # type: Session
        yield logged_http_session


@pytest.fixture(scope="session")
def response(session: Session, session_url: Address) -> Response:
    yield session.get(session_url)


@pytest.fixture(scope="session")
def logged_response(logged_session: Session, session_url: Address) -> Response:
    yield logged_session.get(session_url)


@pytest.fixture()
def users_mock() -> UsersMock:
    with UsersMock(host="0.0.0.0", port=4444) as mock:
        yield mock
