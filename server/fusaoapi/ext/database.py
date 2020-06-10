from flask_mongoengine import MongoEngine
from flask_bcrypt import generate_password_hash, check_password_hash

mongo = MongoEngine()


def init_app(app):
    mongo.init_app(app)


class User(mongo.Document):
    email = mongo.EmailField(required=True, unique=True)
    password = mongo.StringField(required=True, min_length=6)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)
