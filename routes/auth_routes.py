from flask import Blueprint, request, render_template, redirect, flash, url_for
from services.auth_service import AuthService
from forms import LoginForm, SignupForm
from .task_routes import task_routes

auth_routes = Blueprint("auth_routes", __name__)
@auth_routes.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            message, status =  AuthService.signup(username, password)
            if status == 201:
                flash("User created successfully", 'success')
                return render_template("tasks.html", tasks=[])
            else:
                flash(message["message"], 'danger')


    return render_template("signup.html", form=form)

@auth_routes.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            message, status =  AuthService.login(username, password)
            if status == 200:
                return redirect(url_for("task_routes.get_tasks"))
            else:
                flash(message["message"], 'danger')
    return render_template("login.html", form= form)
