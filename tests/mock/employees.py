import socket
import time
from threading import Thread
from types import TracebackType
from typing import Any, Dict, List, Optional, Type

from flask import Flask, Response, json, request

from tests.mock import Endpoint, Mock
from urequest import HTTPStatus, HttpConnectionError, HttpSession, HttpUrl


def _wait_for_connection_ready(
    url: HttpUrl, timeout: int = 10, poll: int = 1
) -> None:
    """Waits for connection to be up and running."""
    end_time = time.time() + timeout
    while end_time > time.time():
        try:
            session = HttpSession()
            session.get(url)
            break
        except HttpConnectionError:
            time.sleep(poll)
    else:
        raise TimeoutError(
            f"Unable to start communication with {url} after {timeout} seconds"
        )


def _wait_for_connection_not_ready(
    host: str, port: int, timeout: int = 5, poll: int = 1
) -> None:
    """Waits for connection to be down."""
    end_time = time.time() + timeout
    while end_time > time.time():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            if conn.connect_ex((host, port)):
                break
        time.sleep(poll)
    else:
        raise TimeoutError(
            f"Unable to stop communication with {host}:{port} "
            f"after {timeout} seconds"
        )


class EmployeesMock(Mock):
    """The class represents a mocked storage server for employees.

    Basically it is used only for unit testing purposes.

    A mock server is started in a separate thread.
    It is required to inject mock in pytest fixtures.
    """

    def __init__(
        self, endpoint: Endpoint, app: Flask = Flask(import_name=__name__)
    ) -> None:
        self._endpoint = endpoint
        self._app = app
        self._users: List[Dict[str, Any]] = []

    @property
    def bind(self) -> str:
        """Returns a binding address of a mock server."""
        return f"{self._endpoint.host}:{self._endpoint.port}"

    def start(self) -> None:
        """Starts an employees mock server."""
        self.__compose_routes()
        thread = Thread(
            target=self._app.run,
            args=(
                self._endpoint.host,
                self._endpoint.port,
                self._endpoint.debug,
            ),
        )
        thread.daemon = True
        thread.start()
        _wait_for_connection_ready(url=HttpUrl(self.bind))

    def clean_up(self) -> None:
        """Cleans up database on server termination."""
        self._users = []

    def __enter__(self) -> Mock:
        """Initializes employees mock server."""
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Terminates employees mock server."""
        self.clean_up()

    def __compose_routes(self) -> None:  # noqa: CFQ001, C901
        """Builds a set of routes for mock server."""

        @self._app.route("/")
        def index() -> Response:
            return self._app.response_class(
                response="Welcome to the employees test app!",
                status=int(HTTPStatus.OK),
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
            new_record = {"id": record_id, **request.json}
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
                    **request.json,
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
