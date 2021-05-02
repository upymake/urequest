# pylint: disable-all
from typing import Iterable
import _pytest.mark
import pytest
from tests.fake.response import FakeHttpResponse
from urequest.response import (
    HTTPStatus,
    Response,
    ResponseError,
    safe_response,
)

pytestmark: _pytest.mark.MarkDecorator = pytest.mark.unittest


@pytest.mark.parametrize(  # noqa: PT006, PT007
    "status, expected",
    (
        pytest.param(
            HTTPStatus.CONTINUE,
            (
                HTTPStatus.CONTINUE,
                HTTPStatus.SWITCHING_PROTOCOLS,
                HTTPStatus.PROCESSING,
            ),
            id="info",
        ),
        pytest.param(
            HTTPStatus.OK,
            (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED),
            id="success",
        ),
        pytest.param(
            HTTPStatus.MULTIPLE_CHOICES,
            (
                HTTPStatus.MULTIPLE_CHOICES,
                HTTPStatus.MOVED_PERMANENTLY,
                HTTPStatus.FOUND,
            ),
            id="redirect",
        ),
        pytest.param(
            HTTPStatus.BAD_REQUEST,
            (
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.UNAUTHORIZED,
                HTTPStatus.PAYMENT_REQUIRED,
            ),
            id="client error",
        ),
        pytest.param(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            (
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.NOT_IMPLEMENTED,
                HTTPStatus.BAD_GATEWAY,
            ),
            id="server error",
        ),
    ),
)
def test_safe_response_code(
    status: HTTPStatus, expected: Iterable[int]
) -> None:
    assert isinstance(
        safe_response(FakeHttpResponse(status), success_codes=expected),
        Response,
    )


def test_safe_response_error() -> None:
    with pytest.raises(ResponseError):
        safe_response(
            FakeHttpResponse(HTTPStatus.INTERNAL_SERVER_ERROR),
            success_codes=(HTTPStatus.OK, HTTPStatus.CREATED),
        )


def test_response_as_json(response: Response) -> None:
    assert response.as_json()


def test_response_is_ok(response: Response) -> None:
    assert response.is_ok()


def test_response_code(response: Response) -> None:
    assert response.status() is HTTPStatus.OK


def test_response_text(response: Response) -> None:
    assert str(response)


def test_logged_response_as_json(logged_response: Response) -> None:
    assert logged_response.as_json()


def test_logged_response_is_ok(logged_response: Response) -> None:
    assert logged_response.is_ok()


def test_logged_response_code(logged_response: Response) -> None:
    assert logged_response.status() is HTTPStatus.OK


def test_logged_response_text(logged_response: Response) -> None:
    assert str(logged_response)
