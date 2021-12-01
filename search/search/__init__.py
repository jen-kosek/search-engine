"""ask485 package initializer."""
import flask

app = flask.Flask(__name__)

import search.model
import search.views
