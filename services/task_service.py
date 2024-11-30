from models.task_model import TaskModel

class TaskService:
    @staticmethod
    def add_task(title, description):
        task = TaskModel.create_task(title, description)
        return {"message": "Task added", "task_id": str(task.inserted_id)}, 201

    @staticmethod
    def get_all_tasks():
        tasks = TaskModel.get_all_tasks()
        return [
            {"id": str(task["_id"]), "title": task["title"], "description": task["description"], "completed": task['completed']}
            for task in tasks
        ], 200

    @staticmethod
    def get_task(task_id):
        task = TaskModel.get_task_by_id(task_id)
        if not task:
            return {"message": "Task not found"}, 404

        return {
            "id": str(task["_id"]),
            "title": task["title"],
            "description": task["description"],
            "completed" : task["completed"]
        }, 200

    @staticmethod
    def update_task(task_id, title, description):
        result = TaskModel.update_task(task_id, title, description)
        if result.matched_count == 0:
            return {"message": "Task not found"}, 404
        return {"message": "Task updated"}, 200
    
    @staticmethod
    def toggle_task(task_id):
        tasks = TaskModel.toggle_completion(task_id)
        print(tasks)
        if not tasks:
            return {"message": "Task not found"}, 404
        
        return {"tasks" : [
            {"id": str(task["_id"]), "title": task["title"], "description": task["description"], "completed": task['completed']}
            for task in tasks
        ]}, 200

    @staticmethod
    def delete_task(task_id):
        result = TaskModel.delete_task(task_id)
        if result.deleted_count == 0:
            return {"message": "Task not found"}, 404
        return {"message": "Task deleted"}, 200
