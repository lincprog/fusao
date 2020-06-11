from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS
from fusaoapi.errors import errors
from .routes import init_routes

bp = Blueprint("fusao", __name__, url_prefix="/api/v1")
api = Api(bp, errors=errors)
CORS(bp)


def init_app(app):
    init_routes(api)
    app.register_blueprint(bp)
