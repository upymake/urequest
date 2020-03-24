"""The module provides API for credentials."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Credentials:
    """The class represents credentials item."""

    username: str
    password: str
