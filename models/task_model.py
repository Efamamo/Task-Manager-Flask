from bson.objectid import ObjectId
from extentions import mongo

class TaskModel:
    @staticmethod
    def create_task(title, description):
        return mongo.db.tasks.insert_one({"title": title, "description": description, "completed": False})

    @staticmethod
    def get_all_tasks():
        return list(mongo.db.tasks.find())

    @staticmethod
    def get_task_by_id(task_id):
        return mongo.db.tasks.find_one({"_id": ObjectId(task_id)})

    @staticmethod
    def update_task(task_id, title, description):
        return mongo.db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"title": title, "description": description}}
        )

    @staticmethod
    def delete_task(task_id):
        return mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})
