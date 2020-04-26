# pylint: disable-all
from typing import Iterable
import _pytest.mark
import pytest
from tests.fake import FakeHttpResponse
from urequest.response import JsonType, Response, ResponseError, safe_response

pytestmark: _pytest.mark.MarkDecorator = pytest.mark.unittest


_content: JsonType = {
    "month": "3",
    "num": 2284,
    "link": "",
    "year": "2020",
    "news": "",
    "safe_title": "Sabotage",
    "transcript": "",
    "alt": "So excited to see everyone after my luxury cruise home from the World Handshake Championships!",
    "img": "https://imgs.xkcd.com/comics/sabotage.png",
    "title": "Sabotage",
    "day": "23",
}


@pytest.mark.parametrize(  # noqa: PT006, PT007
    "code, expected",
    (
        pytest.param(100, (100, 101, 102), id="info"),
        pytest.param(200, (200, 201, 202), id="success"),
        pytest.param(300, (300, 301, 302), id="redirect"),
        pytest.param(400, (400, 401, 402), id="client error"),
        pytest.param(500, (500, 501, 502), id="server error"),
    ),
)
def test_safe_response_code(code: int, expected: Iterable[int]) -> None:
    assert isinstance(safe_response(FakeHttpResponse(code), success_codes=expected), Response)


def test_safe_response_error() -> None:
    with pytest.raises(ResponseError):
        safe_response(FakeHttpResponse(500), success_codes=(200, 201))


def test_response_as_json(response: Response) -> None:
    assert response.as_json()


def test_response_is_ok(response: Response) -> None:
    assert response.is_ok()


def test_response_code(response: Response) -> None:
    assert response.code() == 200


def test_response_text(response: Response) -> None:
    assert str(response)


def test_logged_response_as_json(logged_response: Response) -> None:
    assert logged_response.as_json()


def test_logged_response_is_ok(logged_response: Response) -> None:
    assert logged_response.is_ok()


def test_logged_response_code(logged_response: Response) -> None:
    assert logged_response.code() == 200


def test_logged_response_text(logged_response: Response) -> None:
    assert str(logged_response)
