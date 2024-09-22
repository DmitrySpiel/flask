# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/taskdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

# Route to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(description=data['description'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created!'}), 201

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    result = []
    for task in tasks:
        result.append({
            'id': task.id,
            'description': task.description,
            'is_completed': task.is_completed,
            'created_at': task.created_at
        })
    return jsonify(result), 200

# Route to update task status
@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found!'}), 404
    
    task.is_completed = request.json.get('is_completed', task.is_completed)
    db.session.commit()
    return jsonify({'message': 'Task updated!'}), 200

# New route to delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
