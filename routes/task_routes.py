from flask import Blueprint, request, render_template, redirect, url_for,flash
from services.task_service import TaskService
from flask_jwt_extended import jwt_required
from forms import TasksForm

task_routes = Blueprint("task_routes", __name__)

@task_routes.route("/add", methods=["POST", "GET"])
def add_task():
    form = TasksForm()
    if request.method == "GET":
        return render_template("add_tasks.html", form=form)
    else:
        title = form.title.data
        description = form.description.data
        message, status =  TaskService.add_task(title, description)

        if status == 201:
            flash("Task Added Successfully", 'success')
            return redirect(url_for('task_routes.get_tasks'))
        else:
            flash(message, 'danger')


@task_routes.route("/", methods=["GET"])
# @jwt_required(locations=["cookies"])
def get_tasks():
    tasks, status =  TaskService.get_all_tasks()

    if status == 200:
        return render_template('tasks.html', tasks=tasks)
    else:
        flash(tasks, 'danger')
    


@task_routes.route("/<task_id>", methods=["GET"])
# @jwt_required()
def get_task(task_id):
    task, status =  TaskService.get_task(task_id)
    if status == 200:
        return render_template('task_detail.html', task=task)
    else:
        flash(task, 'danger')

@task_routes.route("/<task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    return TaskService.update_task(task_id, data.get("title"), data.get("description"))

@task_routes.route("/tasks/<task_id>", methods=["POST", 'GET'])
@jwt_required()
def delete_task(task_id):

            
    message, status =  TaskService.delete_task(task_id)

    if status == 200:
        flash("Task Deleted Successfully", 'success')
        return redirect('task_routes.get_tasks')
    else:
        flash(message, 'danger')
