from flask import jsonify, request, redirect, url_for
from app import app, db
from app.user_services import *
from app.models import Task

@app.route('/landing', methods=['GET'])
def landing():
    return jsonify({"message": "Welcome to the API"})


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')

    task = Task(title=title, description=description)
    create = add_task(task,db)
    return create 

    

@app.route("/read", methods=['GET'])
def read_task():
    tasks = Task.query.all()
    get = get_task(tasks.db)
    return get