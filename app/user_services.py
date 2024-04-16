from flask import jsonify
from app import db

def add_task(task):
    try:
        db.session.add(task)
        db.session.commit()
        return jsonify({"message": "Task added successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding task", "error": str(e)})
    

def get_task(tasks):
    try:
        tasks_list = [{"id": task.id, "title": task.title, "description": task.description} for task in tasks]
        return jsonify("message:" "The list of task:", tasks_list)
    except Exception as e:
        return jsonify({"message": "Couldn't get tasks", "error": str(e)})
    