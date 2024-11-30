from bson.objectid import ObjectId
from extentions import mongo

class TaskModel:
    @staticmethod
    def create_task(title, description, userId):
        return mongo.db.tasks.insert_one({"title": title, "description": description, "completed": False, 'owner': ObjectId(userId)})

    @staticmethod
    def get_all_tasks(userId):
        return list(mongo.db.tasks.find({"owner": ObjectId(userId)}))

    @staticmethod
    def get_task_by_id(task_id,user_id):
        return mongo.db.tasks.find_one({"_id": ObjectId(task_id), "owner": ObjectId(user_id) })

    @staticmethod
    def update_task(task_id, title, description):
        return mongo.db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"title": title, "description": description}}
        )
    @staticmethod
    def toggle_completion(task_id):
        task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
        if task:
            new_status = not task.get("completed", False) 
            result = mongo.db.tasks.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": {"completed": new_status}}
            )
            return result.modified_count > 0
        
        return False

    @staticmethod
    def delete_task(task_id):
        return mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})
