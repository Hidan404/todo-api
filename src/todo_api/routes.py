from flask import Blueprint, request, jsonify
from . import db
from .models import Tarefa, Usuario
from .utils import token_obrigatorio

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todos', methods=['GET'])
@token_obrigatorio
def get_todos():
    todos = Tarefa.query.filter_by(usuario_id=request.usuario_id).all()
    return {"todos": [todo.to_dict() for todo in todos]}

@todo_bp.route('/todos', methods=['POST'])
@token_obrigatorio
def create_todo():
    data = request.json
    if not data:
        return jsonify({"erro": "Dados não fornecidos"}), 400

    titulo = data.get('titulo')
    if not titulo:
        return jsonify({"erro": "Título é obrigatório"}), 400

    nova_tarefa = Tarefa(
        titulo=titulo,
        descricao=data.get('descricao', ''),
        usuario_id=request.usuario_id
    )
    db.session.add(nova_tarefa)
    db.session.commit()

    return jsonify(nova_tarefa.to_dict()), 201

@todo_bp.route("/todos/<int:id>", methods=['PUT'])
@token_obrigatorio
def update_todo(id):
    tarefa = Tarefa.query.get_or_404(id)
    if tarefa.usuario_id != request.usuario_id:
        return jsonify({"erro": "Não autorizado"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"erro": "Dados não fornecidos"}), 400

    if 'titulo' in data:
        tarefa.titulo = data['titulo']
    if 'descricao' in data:
        tarefa.descricao = data['descricao']
    if 'concluida' in data:
        tarefa.concluida = data['concluida']

    db.session.commit()
    return jsonify(tarefa.to_dict())

@todo_bp.route("/todos/<int:id>", methods=['DELETE'])
@token_obrigatorio
def delete_todo(id):
    tarefa = Tarefa.query.get_or_404(id)
    if tarefa.usuario_id != request.usuario_id:
        return jsonify({"erro": "Não autorizado"}), 403

    db.session.delete(tarefa)
    db.session.commit()
    return '', 204

@todo_bp.route('/todos/<int:id>', methods=['GET'])
@token_obrigatorio
def get_todo(id):
    tarefa = Tarefa.query.get_or_404(id)
    if tarefa.usuario_id != request.usuario_id:
        return jsonify({"erro": "Não autorizado"}), 403
    return {"todo": tarefa.to_dict()}