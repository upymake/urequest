from typing import Iterable
import pytest
import _pytest.mark
from tests.fake import FakeHttpResponse
from urequest.response import safe_response, ResponseError, Response

pytestmark: _pytest.mark.MarkDecorator = pytest.mark.unittest


@pytest.mark.parametrize(
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
