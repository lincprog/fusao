from flask import Flask

from fusaoapi.ext import auth, database
from fusaoapi import blueprints


def create_app(config_object="fusaoapi.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    database.init_app(app)
    auth.init_app(app)
    blueprints.init_app(app)

    return app
