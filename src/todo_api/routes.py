from flask import Blueprint
from . import db
from .models import Tarefa 

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todos', methods=['GET'])
def get_todos():
    todos = Tarefa.query.all()
    return {"todos": [todo.to_dict() for todo in todos]}

@todo_bp.route('/todos', methods=['POST'])
def create_todo():
    from flask import request, jsonify
    data = request.get_json()
    if not data or 'titulo' not in data:
        return jsonify({"error": "Título é obrigatório"}), 400
    
    nova_tarefa = Tarefa(titulo=data['titulo'], descricao=data['descricao'], concluida=False)
    db.session.add(nova_tarefa)
    db.session.commit()
    
    return jsonify(nova_tarefa.to_dict()), 201

@todo_bp.route("/todos/<int:id>", methods=['PUT'])
def update_todo(id):
    from flask import request, jsonify
    tarefa = Tarefa.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400

    if 'titulo' in data:
        tarefa.titulo = data['titulo']
    if 'descricao' in data:
        tarefa.descricao = data['descricao']
    if 'concluida' in data:
        tarefa.concluida = data['concluida']

    db.session.commit()
    return jsonify(tarefa.to_dict())

@todo_bp.route("/todos/<int:id>", methods=['DELETE'])
def delete_todo(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return '', 204

@todo_bp.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    tarefa = Tarefa.query.get_or_404(id)
    return {"todo": tarefa.to_dict()}   