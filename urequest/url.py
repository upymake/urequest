"""The module provides API for Unified Resource Locator (URL) endpoints."""
from abc import ABC, abstractmethod


class Address(ABC):
    """The class represents an interface of an address."""

    @abstractmethod
    def matcher(self) -> str:
        """Returns a path of the URL."""
        pass

    @abstractmethod
    def host(self) -> str:
        """Returns a domain name (host)."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Returns address as a string."""
        pass


class Url(Address):
    """The class represents regular WEB URL item."""

    def __init__(self, host: str, protocol: str, path: str = "") -> None:
        self._host = host
        self._path = path
        self._protocol = protocol

    def matcher(self) -> str:
        return self._path

    def host(self) -> str:
        return self._host

    def __str__(self) -> str:
        if self._host.startswith(self._protocol):
            return self._host
        return (
            f"{self._protocol}://{self._host}/"
            f"{self._path if not self._path.startswith('/') else self._path[1:]}"
        )


class HttpUrl(Address):
    """The class represents HTTP WEB URL item."""

    def __init__(self, host: str, path: str = "") -> None:
        self._http: Url = Url(host, protocol="http", path=path)

    def matcher(self) -> str:
        return self._http.matcher()

    def host(self) -> str:
        return self._http.host()

    def __str__(self) -> str:
        return str(self._http)


class HttpsUrl(Address):
    """The class represents HTTPS WEB URL item."""

    def __init__(self, host: str, path: str = "") -> None:
        self._https: Url = Url(host, protocol="https", path=path)

    def matcher(self) -> str:
        return self._https.matcher()

    def host(self) -> str:
        return self._https.host()

    def __str__(self) -> str:
        return str(self._https)
