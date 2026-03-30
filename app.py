from __future__ import annotations

import argparse
import io
from urllib.parse import urlencode, urlsplit
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults

from nlp_trainer_support import db
from nlp_trainer_support.config import DEFAULT_HOST, DEFAULT_PORT
from nlp_trainer_support.web import create_app


class SimpleClient:
    def __init__(self, app):
        self.app = app
        self.cookies: dict[str, str] = {}

    def request(self, method: str, path: str, data: dict | None = None):
        split = urlsplit(path)
        body = b""
        if method.upper() == "POST" and data is not None:
            body = urlencode(data, doseq=True).encode("utf-8")

        environ = {}
        setup_testing_defaults(environ)
        environ["REQUEST_METHOD"] = method.upper()
        environ["PATH_INFO"] = split.path
        environ["QUERY_STRING"] = split.query
        environ["CONTENT_LENGTH"] = str(len(body))
        environ["wsgi.input"] = io.BytesIO(body)
        environ["CONTENT_TYPE"] = "application/x-www-form-urlencoded"
        if self.cookies:
            environ["HTTP_COOKIE"] = "; ".join(f"{key}={value}" for key, value in self.cookies.items())

        captured = {}

        def start_response(status, headers, exc_info=None):
            captured["status"] = status
            captured["headers"] = headers

        response_body = b"".join(self.app(environ, start_response))
        for header_name, header_value in captured["headers"]:
            if header_name.lower() == "set-cookie":
                pair = header_value.split(";", 1)[0]
                key, value = pair.split("=", 1)
                self.cookies[key] = value

        return captured["status"], dict(captured["headers"]), response_body.decode("utf-8", errors="ignore")


def run_smoke_test() -> None:
    db.initialize_database(reset=True)
    app = create_app()

    guest = SimpleClient(app)
    status, _headers, body = guest.request("GET", "/")
    assert status.startswith("200"), status
    assert "NLP leren, oefenen en beoordelen" in body

    trainer = SimpleClient(app)
    status, _headers, _body = trainer.request(
        "POST",
        "/login",
        {"email": "trainer@neuroflow.local", "password": "demo123"},
    )
    assert status.startswith("302"), status
    status, _headers, body = trainer.request("GET", "/dashboard")
    assert status.startswith("200"), status
    assert "Begeleiden en beoordelen" in body

    student = SimpleClient(app)
    status, _headers, _body = student.request(
        "POST",
        "/login",
        {"email": "student@neuroflow.local", "password": "demo123"},
    )
    assert status.startswith("302"), status
    status, _headers, body = student.request("GET", "/dashboard")
    assert status.startswith("200"), status
    assert "Jouw leeromgeving" in body

    with db.connect() as connection:
        assignment_id = connection.execute(
            "SELECT id FROM assignments WHERE title = 'Week 1 - Fundamenten en zintuigen'"
        ).fetchone()["id"]
    status, _headers, body = student.request("GET", f"/assignments/{assignment_id}")
    assert status.startswith("200"), status
    assert "Verdiepingspaden ter referentie" in body

    print("Smoke test geslaagd.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the NLP Trainer Support Platform.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", default=DEFAULT_PORT, type=int)
    parser.add_argument("--reset-db", action="store_true", help="Reset the SQLite database before starting.")
    parser.add_argument("--smoke-test", action="store_true", help="Run an internal smoke test and exit.")
    args = parser.parse_args()

    if args.smoke_test:
        run_smoke_test()
        return

    db.initialize_database(reset=args.reset_db)
    app = create_app()
    with make_server(args.host, args.port, app) as server:
        print(f"Server draait op http://{args.host}:{args.port}")
        server.serve_forever()


if __name__ == "__main__":
    main()
