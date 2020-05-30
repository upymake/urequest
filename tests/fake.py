from urequest.response import JsonType, Response


class FakeHttpResponse(Response):
    """The class represents fake HTTP response interface."""

    def __init__(
        self, code: int, is_ok: bool = True, as_str: str = str(), as_dict: JsonType = {}
    ) -> None:
        self._code: int = code
        self._is_ok: bool = is_ok
        self._as_str: str = as_str
        self._as_dict: JsonType = as_dict

    def is_ok(self) -> bool:
        return self._is_ok

    def code(self) -> int:
        return self._code

    def as_json(self) -> JsonType:
        return self._as_dict

    def __str__(self) -> str:
        return self._as_str
