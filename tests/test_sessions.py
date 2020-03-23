import pytest
import _pytest.mark
from urequest.response import Response

pytestmark: _pytest.mark.MarkDecorator = pytest.mark.unittest


def test_response_as_json(response: Response) -> None:
    assert response.as_json() == {
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


def test_response_is_ok(response: Response) -> None:
    assert response.is_ok()


def test_response_code(response: Response) -> None:
    assert response.code() == 200


def test_response_text(response: Response) -> None:
    assert str(response) == (
        '{"month": "3", "num": 2284, "link": "", "year": "2020", "news": "", "safe_title": "Sabotage", '
        '"transcript": "", '
        '"alt": "So excited to see everyone after my luxury cruise home from the World Handshake Championships!", '
        '"img": "https://imgs.xkcd.com/comics/sabotage.png", "title": "Sabotage", "day": "23"}'
    )
