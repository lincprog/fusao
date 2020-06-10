from flask import Blueprint, request, Response
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Api, Resource
from .database import User
import datetime


bp = Blueprint("fusao", __name__, url_prefix="/api/v1")
api = Api(bp)


class UserRegister(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
        id = user.id
        return {"id": str(id)}, 200


class UserLogin(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email=body.get("email"))
        authorized = user.check_password(body.get("password"))
        if not authorized:
            return {"error": "Email or password invalid"}, 401

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(
            identity=str(user.id), expires_delta=expires
        )
        return {"token": access_token}, 200


class UserLogout(Resource):
    def post(self):
        return {"message": "User logout"}


class AllUsers(Resource):
    @jwt_required
    def get(self):
        return {"message": "List of users"}

    @jwt_required
    def delete(self):
        return {"message": "Delete all users"}


def init_app(app):
    api.add_resource(UserRegister, "/signup")
    api.add_resource(UserLogin, "/login")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(AllUsers, "/users")
    app.register_blueprint(bp)
