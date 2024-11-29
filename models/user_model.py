from extentions import mongo

class UserModel:
    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def create_user(username, hashed_password):
        return mongo.db.users.insert_one({"username": username, "password": hashed_password})
