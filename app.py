from flask import Flask
from config import Config
from extentions import bcrypt, jwt, mongo
from routes.auth_routes import auth_routes
from routes.task_routes import task_routes

app = Flask(__name__)
app.config.from_object(Config)

bcrypt.init_app(app)
jwt.init_app(app)
mongo.init_app(app)

app.register_blueprint(auth_routes, url_prefix="/api/v1/auth")
app.register_blueprint(task_routes, url_prefix="/api/v1/tasks")

if __name__ == "__main__":
    app.run()
