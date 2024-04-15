from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

#loads the configurable variables from .env file
load_dotenv()

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

# Define Task model
class Task(db.Model):
    __tablename__ = 'tasks'  # Specify the table name
    __table_args__ = {'schema': 'test'}  # Specify the schema name
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)


@app.route('/landing', methods=['GET'])
def landing():
    return jsonify({"message": "Welcome to the API"})


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task added successfully"})

@app.route("/read", methods=['GET'])
def read_task():
    tasks = Task.query.all()
    tasks_list = [{"id": task.id, "title": task.title, "description": task.description} for task in tasks]
    return jsonify(tasks_list)

if __name__ == '__main__':
    app.run(debug=True)