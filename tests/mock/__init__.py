from abc import abstractmethod
from contextlib import AbstractContextManager
from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoint:
    """The class represents mock server endpoint."""

    host: str
    port: int
    debug: bool = False


class Mock(AbstractContextManager):
    """An abstract interface of a mock server.

    A mock server represents a context manager.
    """

    @property
    @abstractmethod
    def bind(self) -> str:
        """Returns a binding address of a mock server."""
        pass

    @abstractmethod
    def start(self) -> None:
        """Starts an abstract mock server."""
        pass

    @abstractmethod
    def clean_up(self) -> None:
        """Cleans up an abstract mock server data."""
        pass
