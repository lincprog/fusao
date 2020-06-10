
import os

MONGO_URI = os.environ.get('MONGO_URI')
MONGODB_SETTINGS = {'host': MONGO_URI}
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
