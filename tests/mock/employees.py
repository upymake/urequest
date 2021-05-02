from threading import Thread
from types import TracebackType
from typing import Any, Dict, List, Optional, Type

from flask import Flask, Response, json, request

from tests.mock import Mock
from urequest.response import HTTPStatus


class EmployeesMock(Mock):
    """The class represents a mocked storage server for employees.

    Basically it is used only for unit testing purposes.
    """

    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._users: List[Dict[str, Any]] = []
        self._app = Flask(import_name=__name__)

    def __enter__(self) -> Mock:
        """Initializes employees mock server."""
        self.start()
        return self

    @property
    def bind(self) -> str:
        """Returns a binding address of a mock server."""
        return f"{self._host}:{self._port}"

    def start(self) -> None:
        """Starts an employees mock server."""
        self.__compose_routes()
        self._app.run(host=self._host, port=self._port, debug=False)

    def clean_up(self) -> None:
        """Cleans up database on server termination."""
        self._users = []

    def __compose_routes(self) -> None:  # noqa: CFQ001, C901
        """Builds a set of routes for mock server."""

        @self._app.route("/")
        def index() -> Response:
            return self._app.response_class(
                response="Welcome to the employees test app!",
                status=200,
            )

        @self._app.route("/users")
        def users() -> Response:
            return self._app.response_class(
                response=json.dumps(self._users), status=int(HTTPStatus.OK)
            )

        @self._app.route("/create_user", methods=("POST",))
        def create_user() -> Response:
            if not self._users:
                record_id = 0
            else:
                record_id = self._users[len(self._users) - 1]["id"] + 1
            new_record = {"id": record_id, **request.form.to_dict()}
            self._users.append(new_record)
            return self._app.response_class(
                response=json.dumps(new_record), status=int(HTTPStatus.CREATED)
            )

        @self._app.route(
            "/users/<int:user_id>", methods=("GET", "PUT", "DELETE")
        )
        def user(user_id: int) -> Response:
            if request.method == "GET":
                for next_user in self._users:  # type: Dict[str, Any]
                    if user_id == next_user["id"]:
                        return self._app.response_class(
                            response=self._users[user_id],
                            status=int(HTTPStatus.OK),
                        )
                return self._app.response_class(
                    response=f"{user_id} is not found",
                    status=int(HTTPStatus.NOT_FOUND),
                )
            if request.method == "PUT":
                record = {
                    "id": self._users[user_id]["id"],
                    **request.form.to_dict(),
                }
                self._users[user_id] = record
                return self._app.response_class(
                    response=json.dumps(record), status=int(HTTPStatus.OK)
                )
            if request.method == "DELETE":
                self._users.pop(user_id)
                return self._app.response_class(
                    response=json.dumps({}), status=int(HTTPStatus.NO_CONTENT)
                )

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Terminates employees mock server."""
        self.clean_up()


class EmployeesMockThread(Mock):
    """The class represents employees mocked storage server thread.

    Starts mock server in a separate thread.
    It is required to inject mock in pytest fixtures.
    """

    def __init__(self, host: str, port: int) -> None:
        self._mock: Mock = EmployeesMock(host, port)

    def __enter__(self) -> Mock:
        """Initializes employees mock server thread."""
        self.start()
        return self

    @property
    def bind(self) -> str:
        """Returns a binding address of a mock server thread."""
        return self._mock.bind

    def start(self) -> None:
        """Starts employees mock server thread."""
        thread = Thread(target=self._mock.start)
        thread.daemon = True
        thread.start()

    def clean_up(self) -> None:
        """Cleans up employees mock server thread data."""
        self._mock.clean_up()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Terminates employees mock server thread."""
        self.clean_up()
