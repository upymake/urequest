"""Provides user-friendly HTTP client with clean objects."""
from typing import Tuple
from urequest.credentials import Credentials
from urequest.response import JsonType, Response, ResponseError, safe_response
from urequest.session import HttpSession, LoggedHttpSession, Session
from urequest.url import Address, HttpUrl, HttpsUrl, Url

__author__: str = "Volodymyr Yahello"
__email__: str = "vyahello@gmail.com"
__version__: str = "0.0.6"
__license__: str = "MIT License"

__all__: Tuple[str, ...] = (
    "Credentials",
    "Session",
    "HttpSession",
    "LoggedHttpSession",
    "JsonType",
    "Response",
    "ResponseError",
    "safe_response",
    "Address",
    "HttpUrl",
    "HttpsUrl",
    "Url",
)
