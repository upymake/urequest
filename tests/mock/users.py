from types import TracebackType
from typing import Optional, Type

from flask import Flask, Response, json, request

from urequest.response import HTTPStatus


class UsersMock:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._users = [{"id": 0, "name": "Luke", "email": "luke@email.com"}]
        self._app = Flask(__name__)

    def __enter__(self) -> "UsersMock":
        self.start()
        return self

    def start(self) -> None:
        self.__compose_routes()
        self._app.run(host=self._host, port=self._port)

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        del self._app

    def __compose_routes(self) -> None:  # noqa: CFQ001
        @self._app.route("/")
        def index() -> Response:
            return self._app.response_class(
                response=json.dumps({"Intro": "Welcome to the test app!"}),
                status=200,
            )

        @self._app.route("/users")
        def users() -> Response:
            return self._app.response_class(
                response=json.dumps(self._users), status=int(HTTPStatus.OK)
            )

        @self._app.route("/create_user", methods=("POST",))
        def create_user() -> Response:
            last_id = self._users[len(self._users) - 1]["id"]
            new_record = {"id": last_id + 1, **request.form.to_dict()}
            self._users.append(new_record)
            return self._app.response_class(
                response=json.dumps(new_record), status=int(HTTPStatus.ACCEPTED)
            )

        @self._app.route(
            "/users/<int:user_id>", methods=("GET", "PUT", "DELETE")
        )
        def user(user_id: int) -> Response:
            if request.method == "GET":
                return self._app.response_class(
                    response=self._users[user_id], status=int(HTTPStatus.OK)
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
