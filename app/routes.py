from flask import jsonify, request, url_for, redirect
from app import app 
from flask_jwt_extended import get_jwt_identity, create_access_token
from app.user_services import *
from app.models import Task, Users
from passlib.hash import pbkdf2_sha256


@app.route('/', methods=['GET'])
def landing():
    return jsonify({"message": "Welcome to the Page"})


@app.route('/new_task', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    user_id = get_jwt_identity()
    task = Task(title=title, description=description, user_id = user_id)
    create = add_task(task.db)
    return create 

@app.route("/view", methods=['GET'])
def read_task():
    tasks = Task.query.filter_by(user_id=user_id)
    get = get_task(tasks.db)
    return get

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    print(data)    
    
    password_hash = pbkdf2_sha256.hash(password) 

    print(password_hash)

    # Validation
    if not username or not password: 
        return jsonify({'error': 'Missing credentials'}) 

    if Users.query.filter_by(username=username).first():
        return jsonify({'error': 'Username exists'})

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
    
    if not user or not pbkdf2_sha256.verify(password, user.password):  # Check if user exists and password matches
        return jsonify({'error': 'Invalid username or password'}), 401

    # Login successful - Generate JWT and optionally include user_id
    access_token = create_access_token(identity=user.id)
    response = jsonify({
        'message': 'Login successful', 
        'access_token': access_token
    })  
    return response
