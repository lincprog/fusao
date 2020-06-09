from flask_pymongo import PyMongo

mongo = PyMongo()


def init_app(app):
    mongo.init_app(app)
