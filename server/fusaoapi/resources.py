from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from fusaoapi.models import User
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from fusaoapi.errors import (
    SchemaValidationError,
    EmailAlreadyExistsError,
    UnauthorizedError,
    InternalServerError,
    PasswordError,
)
from flask import current_app
from importlib import import_module


parser = reqparse.RequestParser()
parser.add_argument(
    "email",
    type=str,
    help="You need to enter your e-mail address",
    required=True,
)
parser.add_argument(
    "password",
    type=str,
    help="You need to enter your chosen password",
    required=True,
)


class UserRegister(Resource):
    def post(self):
        try:
            parser_register = parser.copy()
            parser_register.add_argument(
                "name",
                type=str,
                help="You need to enter your name",
                required=True,
            )
            parser_register.add_argument(
                "confirmPassword",
                type=str,
                help="You need to enter your confirmPassword",
                required=True,
            )
            data = parser_register.parse_args()
            if data["password"] != data["confirmPassword"]:
                raise PasswordError
            del data["confirmPassword"]
            user = User(**data)
            user.hash_password()
            user.save()
            id = user.id
            return {"id": str(id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except PasswordError:
            raise PasswordError
        except Exception:
            raise InternalServerError


class UserLogin(Resource):
    def post(self):
        try:
            data = parser.parse_args()
            user = User.objects.get(email=data["email"])
            authorized = user.check_password(data["password"])
            if not authorized:
                raise UnauthorizedError

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(
                identity=str(user.id), expires_delta=expires
            )
            return (
                {"token": access_token, "name": user.name, "email": user.email},
                200,
            )
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError


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


class Result(Resource):
    def post(self):
        try:
            parser_name = reqparse.RequestParser()
            parser_name.add_argument(
                "name",
                type=str,
                help="You need to enter Company name",
                required=True,
            )
            parser_name.add_argument(
                "platforms",
                action="append",
                help="You need to enter platforms",
                required=True,
            )
            data = parser_name.parse_args()
            platforms = data["platforms"]
            name = data["name"]
            results = {}
            pl = current_app.config["PLATFORMS"]
            for platform in platforms:
                crawler = import_module(pl[platform])
                results[platform] = crawler.name(name)
            return results
        except Exception:
            raise InternalServerError


class Analysis:
    def post(self):
        try:
            pass
        except Exception:
            raise InternalServerError


class Export:
    def post(self):
        try:
            pass
        except Exception:
            raise InternalServerError
