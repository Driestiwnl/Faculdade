from flask import Flask, jsonify, request

app = Flask(__name__)

# Exemplo de banco de dados (SQLite)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean)

    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    result = []
    for todo in todos:
        todo_data = {'id': todo.id, 'title': todo.title, 'completed': todo.completed}
        result.append(todo_data)
    return jsonify(result)

@app.route('/todos', methods=['POST'])
def create_todo():
    title = request.json['title']
    todo = Todo(title)
    db.session.add(todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message': 'Todo deleted successfully'})
    else:
        return jsonify({'message': 'Todo not found'})

if __name__ == '__main__':
    app.run(debug=True)

import requests
from flask import Flask

app = Flask(__name__)

@app.route('/main/todos', methods=['GET'])
def get_todos():
    response = requests.get('https://jsonplaceholder.typicode.com/todos')
    return response.json()

@app.route('/main/todos', methods=['POST'])
def create_todo():
    payload = {'title': 'New Todo'}
    response = requests.post('https://jsonplaceholder.typicode.com/todos', json=payload)
    return response.json()

@app.route('/main/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    response = requests.delete(f'https://jsonplaceholder.typicode.com/todos')
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
