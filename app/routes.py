from flask import jsonify, request, redirect, url_for, render_template
from app import db, app 
from flask_jwt_extended import create_access_token, jwt_required
from app.user_services import *
from app.models import Task, Users
from passlib.hash import scrypt


@app.route('/', methods=['GET'])
def landing():
    return jsonify({"message": "Welcome to the Page"})


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')

    task = Task(title=title, description=description)
    create = add_task(task.db)
    return create 

@app.route("/read", methods=['GET'])
def read_task():
    tasks = Task.query.all()
    get = get_task(tasks.db)
    return get

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')  # Display the registration form

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password: 
            return jsonify({'error': 'Missing credentials'}), 400 
        if Users.query.filter_by(username=username).first():
            return jsonify({'error': 'Username exists'}), 409

        # Password Hashing using Scrypt
        password_hash = scrypt.hash(password)  
        new_user = Users(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered!'})
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == "GET":
        return render_template('login.html')
    
    if request.method == "POST":
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
             return jsonify({'error': 'Missing username or password'})
        
        user = Users.query.filter_by(username=username).first()
        
        if not user:
             return jsonify({'error': 'Invalid username or password'})
        
        if not scrypt.verify(password, user.password_hash): 
            return jsonify({'error': 'Invalid username or password'})

        access_token = create_access_token(identity=user.id)
        response = jsonify({
            'message': 'Login successful',
            })  

    return response
