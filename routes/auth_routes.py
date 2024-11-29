from flask import Blueprint, request, render_template
from services.auth_service import AuthService
from forms import LoginForm, SignupForm

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            data = request.get_json()
            return AuthService.signup(data.get("username"), data.get("password"))

    return render_template("signup.html", form=form)

@auth_routes.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            data = request.get_json()
            return AuthService.login(data.get("username"), data.get("password"))
    return render_template("login.html", form= form)
