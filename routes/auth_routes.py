from flask import Blueprint, request, render_template, redirect, flash, url_for,jsonify,make_response
from services.auth_service import AuthService
from forms import LoginForm, SignupForm
from .task_routes import task_routes
from flask_jwt_extended import set_access_cookies,unset_access_cookies


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
                return redirect(url_for("auth_routes.login"))
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
           

            message, status = AuthService.login(username, password)
            print(message)
            
            if status == 200:
                access_token = message["token"]
                 
                response = redirect(url_for('task_routes.get_tasks'))
                set_access_cookies(response, access_token)                
                return response
            else:
                flash(message["message"], 'danger')
    
    return render_template("login.html", form=form)

@auth_routes.route("/logout", methods=["GET"])
def logout():
    response = redirect(url_for("auth_routes.login"))
   
    unset_access_cookies(response)
    
    return response

