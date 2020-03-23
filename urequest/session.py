"""The module contains a set of API for HTTP sessions."""
from abc import abstractmethod
from types import TracebackType
from typing import Dict, Any, ContextManager, Optional, Type
import requests
from uyaml.connection import Friendly
from urequest.response import Response, HttpResponse, safe_response
from urequest.url import Address


class Session(Friendly, ContextManager["Session"]):
    """The class represents abstract interfaces for an API Session."""

    @abstractmethod
    def get(self, url: Address, **kwargs: Any) -> Response:
        """Performs ``GET`` HTTP request of a session.

        Args:
            url: url path used to perform a request
            kwargs: keyword arguments

        Returns: response element
        """
        pass

    @abstractmethod
    def options(self, url: Address, **kwargs: Any) -> Response:
        """Performs ``OPTIONS`` HTTP request of a session.

        Args:
            url: url path used to perform a request
            kwargs: keyword arguments

        Returns: response element
        """
        pass

    @abstractmethod
    def head(self, url: Address, **kwargs: Any) -> Response:
        """Performs ``HEAD`` HTTP request of a session.

        Args:
            url: url path used to perform a request
            kwargs: keyword arguments

        Returns: response element
        """
        pass

    @abstractmethod
    def post(self, url: Address, plain: str = None, as_dict: Dict[Any, Any] = None, **kwargs: Any) -> Response:
        """Performs ``POST`` HTTP request of a session.

        Args:
            url: url path used to perform a request
            plain: requested data as a plain text
            as_dict: requested data as dictionary (json)
            kwargs: other keyword arguments

        Returns: response element
        """
        pass

    @abstractmethod
    def put(self, url: Address, plain: str = None, as_dict: Dict[Any, Any] = None, **kwargs: Any) -> Response:
        """Performs ``PUT`` HTTP request of a session.

        Args:
            url: url path used to perform a request
            plain: requested data as a plain text
            as_dict: requested data as dictionary (json)
            kwargs: other keyword arguments

        Returns: response element
        """
        pass

    @abstractmethod
    def patch(self, url: Address, plain: str = None, as_dict: Dict[Any, Any] = None, **kwargs: Any) -> Response:
        """Performs ``PATCH`` HTTP request of a session.

        Args:
            url: url path used to perform a request
            plain: requested data as a plain text
            as_dict: requested data as dictionary (json)
            kwargs: other keyword arguments

        Returns: response element
        """
        pass

    @abstractmethod
    def delete(self, url: Address, **kwargs: Any) -> Response:
        """Performs ``DELETE`` HTTP request of a session.

        Args:
            url: url path used to perform a request
            kwargs: keyword arguments

        Returns: response element
        """
        pass


class HttpSession(Session):
    """The class provides interfaces for current API HTTP session."""

    def __init__(self, session: requests.Session = requests.Session()) -> None:
        self._session: requests.Session = session

    def __enter__(self) -> Session:
        return self

    def get(self, url: Address, **kwargs: Any) -> Response:
        return safe_response(HttpResponse(self._session.get(str(url), **kwargs)))

    def options(self, url: Address, **kwargs: Any) -> Response:
        return safe_response(HttpResponse(self._session.options(str(url), **kwargs)))

    def head(self, url: Address, **kwargs: Any) -> Response:
        return safe_response(HttpResponse(self._session.head(str(url), **kwargs)))

    def post(self, url: Address, plain: str = None, as_dict: Dict[Any, Any] = None, **kwargs: Any) -> Response:
        return safe_response(HttpResponse(self._session.post(str(url), data=plain, json=as_dict, **kwargs)))

    def put(self, url: Address, plain: str = None, as_dict: Dict[Any, Any] = None, **kwargs: Any) -> Response:
        return safe_response(HttpResponse(self._session.put(str(url), data=plain, json=as_dict, **kwargs)))

    def patch(self, url: Address, plain: str = None, as_dict: Dict[Any, Any] = None, **kwargs: Any) -> Response:
        return safe_response(HttpResponse(self._session.patch(str(url), data=plain, json=as_dict, **kwargs)))

    def delete(self, url: Address, **kwargs: Any) -> Response:
        return safe_response(HttpResponse(self._session.delete(str(url), **kwargs)))

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self._session.close()
