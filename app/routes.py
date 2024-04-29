from flask import request, url_for, redirect
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app import app
from app.middleware import MissingCredentialsError, UsernameExistsError, InvalidUsernameOrPassword
from app.models import Task, Users
from app.user_services import *


@app.route('/', methods=['GET'])
def landing():
    return jsonify({"message": "Welcome to the Page"})


@app.route('/new_task', methods=['POST'])
@jwt_required()
def create_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    user_id = get_jwt_identity()

    # Create Task Object (associate with user)
    task = Task(title=title, description=description, user_id=user_id)

    # Call add_task to save to the database
    return add_task(task)


@app.route("/view", methods=['GET'])
@jwt_required()
def read_task():
    user_id = get_jwt_identity()  # Will be None if no valid token

    if user_id:
        tasks = Task.query.filter_by(user_id=user_id).all()
        return get_task(tasks)

    else:
        # Handle non-logged in scenario
        print((jsonify({'error': 'Login required'}), 401))
        return redirect(url_for('login'))


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    reg(data)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    log(data)
