# pylint: disable-all
import pytest
from urequest.credentials import Credentials

pytestmark = pytest.mark.unittest


def test_username(credentials: Credentials) -> None:
    assert credentials.username == "superuser"


def test_password(credentials: Credentials) -> None:
    assert credentials.password == "superpass"


def test_as_string(credentials: Credentials) -> None:
    assert (
        str(credentials) == "Credentials("
        "username='superuser', password='superpass')"
    )
