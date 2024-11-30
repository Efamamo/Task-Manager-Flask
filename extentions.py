from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

bcrypt = Bcrypt()
jwt = JWTManager()
mongo = PyMongo()

def init_extensions(app):
    bcrypt.init_app(app)
    jwt.init_app(app)
    mongo.init_app(app)
