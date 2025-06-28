from flask import Blueprint, request, jsonify
from . import db
from .models import Tarefa 

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todos', methods=['GET'])
def get_todos():
    todos = Tarefa.query.all()
    return {"todos": [todo.to_dict() for todo in todos]}

@todo_bp.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    
    # Validação aprimorada
    if not data:
        return jsonify({"erro": "Dados não fornecidos"}), 400
    
    titulo = data.get('titulo')
    usuario_id = data.get('usuario_id')
    
    if not titulo:
        return jsonify({"erro": "Título é obrigatório"}), 400
    if not usuario_id:
        return jsonify({"erro": "ID do usuário é obrigatório"}), 400
    
    # Verificar se o usuário existe
    from .models import Usuario
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    
    nova_tarefa = Tarefa(
        titulo=titulo,
        descricao=data.get('descricao', ''),
        usuario_id=usuario_id
    )
    
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