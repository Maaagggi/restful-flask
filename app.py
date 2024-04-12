from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Task 1", "Velai iruku": "Description for Task 1"},
    {"id": 2, "title": "Task 2", "Velai illa": "Description for Task 2"}
]

@app.route("/")
def index():
    return 'VANAKAM'

@app.route('/tasks/addmore', methods=['POST'])
def add_task():
    task = request.json
    tasks.append(task)
    return jsonify({"message": "Task added succesfully"})

@app.route('/tasks', methods = ['GET'])
def get_task():
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_ID):
    for task in tasks:
        if task['id'] == task_ID:
            data = request.json
            task.update(data)
            return jsonify({"message": "WORK AIDUCHU DAW"})
        return jsonify({"messsge": "work aavalaye"}
        )

@app.route('/tasks/<int:task_id>/delete', methods = ['DELETE'])
def delete_task(task_ID):
    for task in tasks:
        if task['id'] == task_ID:
            data = request.json
            task.delete(data)
        return jsonify({"message:", "Delete aiduchu!!!"})
    return jsonify({"message:", "Listlaye illa"})


if __name__ == '__main__':
    app.run(debug=True)