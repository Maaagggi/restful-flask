from flask import jsonify
from app import db
# from models import Users
from .models import Users



def add_task(task):
    try:
        db.session.add(task)
        db.session.commit()
        return jsonify({'message': 'Task created', 'task_id': task.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding task", "error": str(e)})
    

def get_task(tasks):
    try:
        tasks_list = [{"id": task.id, "title": task.title, "description": task.description} for task in tasks]
        return jsonify("message:" "The list of task:", tasks_list)
    except Exception as e:
        return jsonify({"message": "Couldn't get tasks", "error": str(e)})
    
def register():
    
    try:
        if not username or not password: 

            return jsonify({'error': 'Missing credentials'}), 400 
        
        if Users.query.filter_by(username=username).first():

            return jsonify({'error': 'Username exists'}), 409

        # Password Hashing using Scrypt
        password = pbkdf2_sha256.hash(password)  
        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered!'})
    
    except Exception as e:

        return jsonify({'error': 'Error registering user', 'error': str(e)})