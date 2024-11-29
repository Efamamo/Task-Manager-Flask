from extentions import bcrypt
from models.user_model import UserModel
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def signup(username, password):
        if UserModel.find_by_username(username):
            return {"message": "User already exists"}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        UserModel.create_user(username, hashed_password)
        return {"message": "User created successfully"}, 201

    @staticmethod
    def login(username, password):
        user = UserModel.find_by_username(username)
        if not user or not bcrypt.check_password_hash(user["password"], password):
            return {"message": "Invalid username or password"}, 401

        token = create_access_token(identity=str(user["_id"]))
        return {"token": token}, 200
