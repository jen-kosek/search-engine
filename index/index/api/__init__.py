"""Index REST API."""

from index.api.routes import get_services
from index.api.routes import get_hits
import os
import app

app.config["INDEX_PATH"] = os.getenv("INDEX_PATH")
