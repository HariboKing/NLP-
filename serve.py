from __future__ import annotations

import os
from wsgiref.simple_server import make_server

import nlp_trainer_support.branding_extension  # noqa: F401
import nlp_trainer_support.deletion_extension  # noqa: F401
import nlp_trainer_support.game_extension  # noqa: F401
import nlp_trainer_support.game_map_extension  # noqa: F401
import nlp_trainer_support.reviews_extension  # noqa: F401
import nlp_trainer_support.world_models_extension  # noqa: F401
import nlp_trainer_support.content_admin_extension  # noqa: F401
import nlp_trainer_support.content_editor_access_extension  # noqa: F401
import nlp_trainer_support.content_question_management_extension  # noqa: F401
import nlp_trainer_support.content_media_extension  # noqa: F401
from nlp_trainer_support.config import DEFAULT_HOST, DEFAULT_PORT
from nlp_trainer_support.runtime_setup import initialize_runtime_database
from nlp_trainer_support.web import create_app


def main() -> None:
    initialize_runtime_database()
    app = create_app()
    host = os.getenv("HOST", DEFAULT_HOST)
    port = int(os.getenv("PORT", str(DEFAULT_PORT)))

    try:
        from waitress import serve
    except ImportError:
        with make_server(host, port, app) as server:
            print(f"Fallback server draait op http://{host}:{port}")
            server.serve_forever()
        return

    print(f"Waitress server draait op http://{host}:{port}")
    serve(app, host=host, port=port, threads=8)


if __name__ == "__main__":
    main()
