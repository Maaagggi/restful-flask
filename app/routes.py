from flask import jsonify, request, url_for, redirect
from app import app 
from flask_jwt_extended import get_jwt_identity, create_access_token
from flask_jwt_extended import jwt_required

from app.user_services import *
from app.models import Task, Users
from passlib.hash import pbkdf2_sha256


class MissingCredentialsError(Exception):
    pass

class UsernameExistsError(Exception):
    pass

class InvalidUsernameOrPassword(Exception):
    pass

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
@jwt_required(optional=True)  # Attempt to verify JWT (if present)
def read_task():
    user_id = get_jwt_identity()  # Will be None if no valid token

    if user_id:
        tasks = Task.query.filter_by(user_id=user_id).all()
        # Use your existing get_task function (if preferred)
        return get_task(tasks)

    else:
        # Handle non-logged in scenario
        result = (jsonify({'error': 'Login required'}), 401 )
        return redirect(url_for('login'))


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    password_hash = pbkdf2_sha256.hash(password) 

    # Validation
    if not username or not password: 
        raise MissingCredentialsError('Missing credentials') 

    if Users.query.filter_by(username=username).first():
        raise UsernameExistsError('Username exists')

    # Create user and save to database
    new_user = Users(username=username, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered!'})

    
    
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = Users.query.filter_by(username=username).first()  # Fetch the user  
    
    print(user.password)

    if not user or not pbkdf2_sha256.verify(password, user.password):  # Check if user exists and password matches
        raise InvalidUsernameOrPassword('Invalid Username or Password')

    # Login successful - Generate JWT and optionally include user_id
    access_token = create_access_token(identity=user.id)
    return jsonify (access_token=access_token)