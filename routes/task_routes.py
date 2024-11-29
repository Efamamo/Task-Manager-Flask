from flask import Blueprint, request
from services.task_service import TaskService
from flask_jwt_extended import jwt_required

task_routes = Blueprint("task_routes", __name__)

@task_routes.route("/", methods=["POST"])
@jwt_required()
def add_task():
    data = request.get_json()
    return TaskService.add_task(data.get("title"), data.get("description", ""))

@task_routes.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    return TaskService.get_all_tasks()

@task_routes.route("/<task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    return TaskService.get_task(task_id)

@task_routes.route("/<task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    return TaskService.update_task(task_id, data.get("title"), data.get("description"))

@task_routes.route("/tasks/<task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    return TaskService.delete_task(task_id)
