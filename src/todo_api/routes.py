from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.todo_api.errors import APIError
from . import db
from .models import Tarefa, Usuario
<<<<<<< HEAD
from .utils import token_obrigatorio
=======
>>>>>>> a30c9bc4ebd28743636eb8a7cde616b52c194906

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todos', methods=['GET'])
<<<<<<< HEAD
@token_obrigatorio
def get_todos():
    todos = Tarefa.query.filter_by(usuario_id=request.usuario_id).all()
    return {"todos": [todo.to_dict() for todo in todos]}

@todo_bp.route('/todos', methods=['POST'])
@token_obrigatorio
=======
@jwt_required()
def get_todos():
    # Obtém o ID do usuário a partir do token JWT
    usuario_id = get_jwt_identity()
    
    # Busca apenas as tarefas do usuário autenticado
    tarefas = Tarefa.query.filter_by(usuario_id=usuario_id).all()
    
    return jsonify({
        "sucesso": True,
        "total": len(tarefas),
        "tarefas": [tarefa.to_dict() for tarefa in tarefas]
    })

@todo_bp.route('/todos', methods=['POST'])
@jwt_required()
>>>>>>> a30c9bc4ebd28743636eb8a7cde616b52c194906
def create_todo():
    usuario_id = get_jwt_identity()
    data = request.json
<<<<<<< HEAD
    if not data:
        return jsonify({"erro": "Dados não fornecidos"}), 400

    titulo = data.get('titulo')
    if not titulo:
        return jsonify({"erro": "Título é obrigatório"}), 400

=======
    
    # Validação básica
    if not data:
        raise APIError("Dados não fornecidos", 400)
    
    titulo = data.get('titulo')
    
    # Validação de campos obrigatórios
    if not titulo:
        raise APIError("Título é obrigatório", 400)
    
    # Verificar se o usuário existe
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        raise APIError("Usuário não encontrado", 404)
    
    # Cria a nova tarefa
>>>>>>> a30c9bc4ebd28743636eb8a7cde616b52c194906
    nova_tarefa = Tarefa(
        titulo=titulo,
        descricao=data.get('descricao', ''),
        usuario_id=request.usuario_id
    )
<<<<<<< HEAD
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
=======
    
    try:
        db.session.add(nova_tarefa)
        db.session.commit()
        
        return jsonify({
            "sucesso": True,
            "mensagem": "Tarefa criada com sucesso",
            "tarefa": nova_tarefa.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        raise APIError("Erro ao criar tarefa", 500)

@todo_bp.route("/todos/<int:id>", methods=['PUT'])
@jwt_required()
def update_todo(id):
    usuario_id = get_jwt_identity()
    
    # Busca a tarefa e verifica permissão
    tarefa = Tarefa.query.get(id)
    if not tarefa:
        raise APIError("Tarefa não encontrada", 404)
    
    if tarefa.usuario_id != usuario_id:
        raise APIError("Acesso não autorizado", 403)
    
    data = request.get_json()
    if not data:
        raise APIError("Dados não fornecidos", 400)
    
    # Validação de campos
    erros = {}
    if 'titulo' in data and not data['titulo']:
        erros['titulo'] = "Título não pode ser vazio"
    
    if 'concluida' in data and not isinstance(data['concluida'], bool):
        erros['concluida'] = "O campo concluída deve ser booleano"
    
    if erros:
        raise APIError("Dados inválidos", 400, payload={"erros": erros})
    
    # Atualiza os campos permitidos
    campos_permitidos = ['titulo', 'descricao', 'concluida']
    for campo in campos_permitidos:
        if campo in data:
            setattr(tarefa, campo, data[campo])
    
    try:
        db.session.commit()
        return jsonify({
            "sucesso": True,
            "mensagem": "Tarefa atualizada",
            "tarefa": tarefa.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        raise APIError("Erro ao atualizar tarefa", 500)

@todo_bp.route("/todos/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    usuario_id = get_jwt_identity()
    
    # Busca a tarefa e verifica permissão
    tarefa = Tarefa.query.get(id)
    if not tarefa:
        raise APIError("Tarefa não encontrada", 404)
    
    if tarefa.usuario_id != usuario_id:
        raise APIError("Acesso não autorizado", 403)
    
    try:
        db.session.delete(tarefa)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        raise APIError("Erro ao excluir tarefa", 500)

@todo_bp.route('/todos/<int:id>', methods=['GET'])
@jwt_required()
def get_todo(id):
    usuario_id = get_jwt_identity()
    
    # Busca a tarefa e verifica permissão
    tarefa = Tarefa.query.get(id)
    if not tarefa:
        raise APIError("Tarefa não encontrada", 404)
    
    if tarefa.usuario_id != usuario_id:
        raise APIError("Acesso não autorizado", 403)
    
    return jsonify({
        "sucesso": True,
        "tarefa": tarefa.to_dict()
    })
>>>>>>> a30c9bc4ebd28743636eb8a7cde616b52c194906
