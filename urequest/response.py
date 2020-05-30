"""The module contains a set of API for HTTP responses types."""
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, Dict, Iterable, Union
import requests

JsonType = Union[Dict[Any, Any], Any]


class ResponseError(Exception):
    """The class represents HTTP api request response error."""

    pass


class Response(ABC):
    """The class represents an abstraction of a response from an API request."""

    @abstractmethod
    def is_ok(self) -> bool:
        """Returns `True` if response is `OK` otherwise `False`."""
        pass

    @abstractmethod
    def code(self) -> HTTPStatus:
        """Returns HTTP response status code."""
        pass

    @abstractmethod
    def as_json(self) -> JsonType:
        """Returns HTTP response data as dictionary type."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Returns HTTP response data as plain data type."""
        pass


class HttpResponse(Response):
    """The class represents an HTTP response from HTTP API request."""

    def __init__(self, response: requests.Response) -> None:
        self._response: requests.Response = response

    def is_ok(self) -> bool:
        return self._response.ok

    def code(self) -> HTTPStatus:
        return HTTPStatus(self._response.status_code)

    def as_json(self) -> JsonType:
        return self._response.json()

    def __str__(self) -> str:
        return self._response.text


def safe_response(
    response: Response,
    success_codes: Iterable[int] = (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.NO_CONTENT),
) -> Response:
    """Specifies safe response from iterable of success HTTP status codes.

    Args:
        response: a specific HTTP response
        success_codes: a list of allowed success codes

    Raises:
        `ResponseError` if HTTP response contains a set of errors

    Returns: a response
    """
    if response.code() not in success_codes:
        raise ResponseError(
            f"HTTP response contains some errors with '{response.code()}' "
            f"status code! Reason: {response}"
        )
    return response
