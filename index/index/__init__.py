"""Init file for index."""
import os
import flask


app = flask.Flask(__name__)
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH")

import index.api  # noqa: E402 pylint: disable=wrong-import-position
