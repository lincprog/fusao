from flask import Blueprint
from flask_restful import Api, Resource


bp = Blueprint("fusao", __name__, url_prefix="/api/v1")
api = Api(bp)


class UserRegister(Resource):
    def post(self):
        return {"message": "User registration"}


class UserLogin(Resource):
    def post(self):
        return {"message": "User login"}


class UserLogout(Resource):
    def post(self):
        return {"message": "User logout"}


class AllUsers(Resource):
    def get(self):
        return {"message": "List of users"}

    def delete(self):
        return {"message": "Delete all users"}


def init_app(app):
    api.add_resource(UserRegister, "/signup")
    api.add_resource(UserLogin, "/login")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(AllUsers, "/users")
    app.register_blueprint(bp)
