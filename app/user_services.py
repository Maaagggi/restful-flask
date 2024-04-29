from flask import jsonify
from flask_jwt_extended import create_access_token
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app import db
from app.middleware import InvalidUsernameOrPassword, UsernameExistsError, MissingCredentialsError
from app.models import Users


def add_task(task):
    try:
        db.session.add(task)
        db.session.commit()
        return jsonify({'status': 'Success',
                        'message': 'Task added successfully',
                        'data': {'task_id': task.id}})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding task", "error": str(e)})


def get_task(tasks):
    try:
        tasks_list = [{"id": task.id, "title": task.title, "description": task.description} for task in tasks]
        return jsonify({'status': 'Success',
                        'message': 'Listing tasks',
                        'data': {'tasks': tasks_list}})

    except Exception as e:
        return jsonify({"message": "Couldn't get tasks", "error": str(e)})


def log(data):
    username = data.get('username')
    password = data.get('password')

    user = Users.query.filter_by(username=username).first()  # Fetch the user

    if not user or not pbkdf2_sha256.verify(password, user.password):
        raise InvalidUsernameOrPassword('Invalid Username or Password')

    # Login successful - Generate JWT and optionally include user_id
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


def reg(data):
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
