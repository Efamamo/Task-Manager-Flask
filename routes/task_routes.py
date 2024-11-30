from flask import Blueprint, request, render_template, redirect, url_for,flash
from services.task_service import TaskService
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from forms import TasksForm
from wtforms.fields import Label
from flask_jwt_extended.exceptions import  (
    NoAuthorizationError,
    InvalidHeaderError,
    JWTDecodeError,
    WrongTokenError,
    RevokedTokenError,
    FreshTokenRequired,
    
)
from functools import wraps



task_routes = Blueprint("task_routes", __name__)

def jwt_required_with_redirect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except NoAuthorizationError:
            flash("Please login to continue", "warning")
            return redirect(url_for('auth.login'))
        except InvalidHeaderError:
            flash("Invalid authentication header. Please login again.", "warning")
            return redirect(url_for('auth.login'))
        except JWTDecodeError:
            flash("Invalid token. Please login again.", "warning")
            return redirect(url_for('auth.login'))
        except WrongTokenError:
            flash("Wrong token type. Please login again.", "warning")
            return redirect(url_for('auth.login'))
        except RevokedTokenError:
            flash("Token has been revoked. Please login again.", "warning")
            return redirect(url_for('auth.login'))
        except FreshTokenRequired:
            flash("Fresh login required. Please login again.", "warning")
            return redirect(url_for('auth.login'))
      
        except Exception as e:
            flash("Authentication error. Please login again.", "warning")
            return redirect("/api/v1/auth/login")
    return decorated_function

@task_routes.route("/add", methods=["POST", "GET"])
@jwt_required_with_redirect 
def add_task():
    current_user_id = get_jwt_identity()
    form = TasksForm()
    if request.method == "GET":
        return render_template("add_tasks.html", form=form)
    else:
        title = form.title.data
        description = form.description.data
        message, status =  TaskService.add_task(title, description,current_user_id)

        if status == 201:
            flash("Task Added Successfully", 'success')
            return redirect(url_for('task_routes.get_tasks'))
        else:
            flash(message, 'danger')


@task_routes.route("/", methods=["GET"])
@jwt_required_with_redirect 
def get_tasks():
    current_user_id = get_jwt_identity()
    print(current_user_id)
    tasks, status =  TaskService.get_all_tasks(current_user_id)

    if status == 200:
        return render_template('tasks.html', tasks=tasks)
    else:
        flash(tasks, 'danger')
    


@task_routes.route("/<task_id>", methods=["GET"])
@jwt_required_with_redirect
def get_task(task_id):
    current_user_id = get_jwt_identity()

    task, status =  TaskService.get_task(task_id,current_user_id)
    if status == 200:
        return render_template('task_detail.html', task=task)
    else:
        flash(task["message"], 'danger')
        return redirect(url_for('task_routes.get_tasks'))

@task_routes.route("/<task_id>/edit", methods=["POST", "GET"])
@jwt_required_with_redirect
def update_task(task_id):
    current_user_id = get_jwt_identity()
    task, status = TaskService.get_task(task_id,current_user_id)
    if status != 200:
        flash("Task not found", "danger")
        return redirect(url_for('task_routes.get_tasks'))
    
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
            return redirect(url_for('task_routes.get_task', task_id=task_id))
        else:
            flash(message, "danger")
            return render_template('edit.html', form=form, task=task)

    return render_template('edit.html', form=form, task=task)

@task_routes.route("/<task_id>/toggle")
def toggle_task(task_id):
    tasks, status = TaskService.toggle_task(task_id)
    path = request.args.get('path')
    
    if status == 200:
        if path == 'single':
            return redirect(url_for('task_routes.get_task', task_id=task_id))

        return redirect(url_for('task_routes.get_tasks')) 
    else:
        flash("Failed to update task", 'danger')
        if path == 'single':
            return redirect(url_for('task_routes.get_task', task_id=task_id))
        return redirect(url_for('task_routes.get_tasks')) 


@task_routes.route("/<task_id>", methods=["POST"])
def delete_task(task_id):    
    message, status =  TaskService.delete_task(task_id)

    if status == 200:
        flash("Task Deleted Successfully", 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('task_routes.get_tasks'))

