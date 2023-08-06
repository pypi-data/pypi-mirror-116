"""Notelist package.

Notelist is a tag based note taking REST API that can be used to manage
notebooks, tags and notes. Notelist is based on the Flask framework.
"""

from datetime import timedelta

from flask import Flask, request, render_template, abort
from flask.wrappers import Response
from flask_migrate import Migrate

from notelist.config import sm
from notelist.auth import jwt
from notelist.db import db, ma
from notelist.views import register_blueprints
from notelist.errors import register_error_handlers
from notelist.cli import add_commands


__version__ = "0.6.0"

# Application object
app = Flask(__name__)
app.secret_key = sm.get("NOTELIST_SECRET_KEY")

app.config["JSON_SORT_KEYS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = sm.get("NOTELIST_DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# Database, object serialization and database migrations
db.init_app(app)
ma.init_app(app)
mig = Migrate(app, db)

# User authentication (JWT)
jwt.init_app(app)

# Blueprints (view groups) and errors
register_blueprints(app)
register_error_handlers(app)

# Commands
add_commands(app)


@app.route("/", methods=["GET"])
def index() -> str:
    """Return the API documentation page.

    The documentation page is returned only if the "NOTELIST_ROOT_DOC"
    environment variable is set and its value is "yes". Otherwise, a HTML 404
    error (Not Found) response is returned.

    :return: Documentation page (HTML code).
    """
    if sm.get("NOTELIST_ROOT_DOC") != "yes":
        return abort(404)

    return render_template(
        "index.html", version=__version__, host_url=request.host_url)


@app.after_request
def after_request(response: Response) -> Response:
    """Modify each request response before sending it.

    This function sets the "Access-Control-Allow-Origin" and
    "Access-Control-Allow-Headers" headers in every response of the API before
    sending it. These headers are related to CORS (Cross-Origin Resource
    Sharing).

    ### CORS (Cross-Origin Resource Sharing):

    The value of the "Access-Control-Allow-Origin" response header determines
    which host is allow to make requests to the API from a front-end
    application (from JavaScript code).

    If this API is used through a front-end application and the API and the
    front-end application are in the same host, then it's not needed to set
    this header. If the API and the front-end are in different hosts, then the
    header must be set to the host of the front-end application (starting with
    "https://").

    The value "*" for the header allows a front-end from any host to make
    requests to the API but this is not recommended and is not supported by all
    browsers.

    In this API, the value of the header is set through the
    "NOTELIST_ALLOW_ORIGIN" environment variable.

    :param response: Original response.
    :return: Final response.
    """
    response.access_control_allow_origin = sm.get("NOTELIST_ALLOW_ORIGIN")
    response.access_control_allow_headers = [
        "Accept", "Content-Type", "Authorization"]

    return response
