import pytest
from urequest.response import Response
from urequest.session import Session, HttpSession
from urequest.url import HttpUrl


@pytest.fixture(scope="session")
def session() -> Session:
    with HttpSession() as http_session:  # type: Session
        yield http_session


@pytest.fixture(scope="session")
def response(session: Session) -> Response:
    yield session.get(HttpUrl(host="xkcd.com", path="info.0.json"))
