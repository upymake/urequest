# pylint: disable-all
import _pytest.mark
import pytest
from urequest.url import Address, HttpUrl, HttpsUrl, Url

_host: str = "9.9.9.9"
_path: str = "/api/path"

pytestmark: _pytest.mark.MarkDecorator = pytest.mark.unittest


@pytest.fixture(scope="module")
def url() -> Address:
    return Url(_host, protocol="ftp", path=_path)


@pytest.fixture(scope="module")
def http_url() -> Address:
    return HttpUrl(_host, _path)


@pytest.fixture(scope="module")
def https_url() -> Address:
    return HttpsUrl(_host, _path)


def test_url_with_leading_slash() -> None:
    assert str(Url(_host, protocol="ftp", path="/w/r")) == f"ftp://{_host}/w/r"


def test_url_without_leading_slash() -> None:
    assert str(Url(_host, protocol="ftp", path="w/r")) == f"ftp://{_host}/w/r"


def test_url_with_full_host_path() -> None:
    assert (
        str(Url(f"ftp://{_host}/w/r", protocol="ftp")) == f"ftp://{_host}/w/r"
    )


def test_url_host(url: Address) -> None:
    assert url.host() == _host


def test_url_matcher(url: Address) -> None:
    assert url.matcher() == _path


def test_url_as_str(url: Address) -> None:
    assert str(url) == f"ftp://{_host}{_path}"


def test_http_url_host(http_url: Address) -> None:
    assert http_url.host() == _host


def test_http_url_matcher(http_url: Address) -> None:
    assert http_url.matcher() == _path


def test_http_url_as_str(http_url: Address) -> None:
    assert str(http_url) == f"http://{_host}{_path}"


def test_https_url_host(https_url: Address) -> None:
    assert https_url.host() == _host


def test_https_url_matcher(https_url: Address) -> None:
    assert https_url.matcher() == _path


def test_https_url_as_str(https_url: Address) -> None:
    assert str(https_url) == f"https://{_host}{_path}"
