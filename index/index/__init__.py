"""Init file"""
import flask
import os

app = flask.Flask(__name__)
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH")
