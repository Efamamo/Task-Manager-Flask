from flask import Blueprint, request, render_template, redirect, url_for,flash
from services.task_service import TaskService
from flask_jwt_extended import jwt_required
from forms import TasksForm
from wtforms.fields import Label


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

@task_routes.route("/<task_id>/edit", methods=["POST", "GET"])
def update_task(task_id):
    task, status = TaskService.get_task(task_id)
    if status != 200:
        flash("Task not found", "danger")
        return redirect(url_for('task_routes.get_tasks'))
    
    # Create an empty form
    form = TasksForm()

    if request.method == 'GET':
        form.title.data = task.get('title')
        form.description.data = task.get('description')
        form.submit.label = Label('submit', 'Edit Task')

        
        return render_template('edit.html', form=form, task=task)

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        message, status = TaskService.update_task(task_id, title, description)
        
        if status == 200:
            flash("Task updated successfully", "success")
            return redirect(url_for('task_routes.get_tasks'))
        else:
            flash(message, "danger")
            return render_template('edit.html', form=form, task=task)

    return render_template('edit.html', form=form, task=task)

@task_routes.route("/<task_id>/toggle", methods=["GET", "PUT"])
def toggle_task(task_id):
    tasks, status = TaskService.toggle_task(task_id)
    
    if status == 200:
        flash("Task Updated Successfully", 'success')
        return redirect(url_for('task_routes.get_tasks'))  # Assuming get_tasks route shows all tasks
    else:
        flash("Failed to update task", 'danger')
        return redirect(url_for('task_routes.get_tasks'))  # Fallback redirect


@task_routes.route("/<task_id>", methods=["POST"])
def delete_task(task_id):    
    message, status =  TaskService.delete_task(task_id)

    if status == 200:
        flash("Task Deleted Successfully", 'success')
        return redirect(url_for('task_routes.get_tasks'))
    else:
        flash(message, 'danger')
