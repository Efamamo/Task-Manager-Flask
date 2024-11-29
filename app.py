from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/taskmanager"  
app.config["JWT_SECRET_KEY"] = "hellothisisstronjwtsecret" 

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mongo = PyMongo(app)

users_collection = mongo.db.users
tasks_collection = mongo.db.tasks


# Validates if the object id is correct
def is_valid_objectid(objectid):
    try:
        ObjectId(objectid)
        return True
    except:
        return False


# Signs up the users
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"message": "username is taken"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {"username": username, "password": hashed_password}

    users_collection.insert_one(user)

    return jsonify({"message": "User created successfully"}), 201

# Logs user in 
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = users_collection.find_one({"username": username})
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Unauthorized"}), 401

    
    access_token = create_access_token(identity=str(user["_id"]))
    return jsonify({"access_token": access_token}), 201


# Add task
@app.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', "")

    if not title:
        return jsonify({"message": "Title is required"}), 400

    task = {"title": title, "description": description}
    tasks_collection.insert_one(task)

    return jsonify({
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"]
    }), 201


# Fetchs all tasks
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = []
    for task in tasks_collection.find():
        tasks.append({
            "id": str(task["_id"]),
            "title": task["title"],
            "description": task["description"]
        })

    return jsonify(tasks), 200



# Fetchs single task by id
@app.route('/tasks/<task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    if not is_valid_objectid(task_id):
        return jsonify({"message": "Invalid task ID"}), 400

    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        return jsonify({"message": "Task not found"}), 404

    return jsonify({
            "id": str(task["_id"]),
            "title": task["title"],
            "description": task["description"]
        }), 200



# Updates a task
@app.route('/tasks/<task_id>', methods=['PATCH'])
@jwt_required()
def update_task(task_id):
    if not is_valid_objectid(task_id):
        return jsonify({"message": "Invalid task ID"}), 400


    updated_task = {}
   
    data = request.get_json()
    title = data.get('title','')

    if title:
        updated_task["title"] = title
    
    description = data.get('description','')
    if description:
        updated_task["description"] = description

    
    result = tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": updated_task})

    if result.matched_count == 0:
        return jsonify({"message": "Task not found"}), 404

    return jsonify({"message": "Task updated"}), 200


# Deletes a task
@app.route('/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    if not is_valid_objectid(task_id):
        return jsonify({"message": "Invalid task ID"}), 400

    result = tasks_collection.delete_one({"_id": ObjectId(task_id)})

    if result.deleted_count == 0:
        return jsonify({"message": "Task not found"}), 404

    return jsonify({"message": "Task deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
