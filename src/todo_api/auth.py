from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from todo_api.routes import token_obrigatorio
from . import db
from .models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    nome = data.get('nome')

    if not email or not senha or not nome:
        return jsonify({"erro": "Dados incompletos"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "Email já registrado"}), 400

    novo_usuario = Usuario(nome=nome, email=email)
    novo_usuario.set_senha(senha)

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário registrado com sucesso"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    from flask import current_app
    import jwt
    import datetime

    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"erro": "Credenciais inválidas"}), 401

    print("DEBUG SECRET_KEY:", repr(current_app.config.get('SECRET_KEY')))  # <- linha de debug

    secret = current_app.config.get('SECRET_KEY')
    if not isinstance(secret, str):
        return jsonify({"erro": "SECRET_KEY inválida"}), 500

    token = jwt.encode({
        'usuario_id': usuario.id,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
    }, secret, algorithm='HS256')

    return jsonify({"token": token}), 200


@auth_bp.route('/me', methods=['GET'])
@token_obrigatorio
def me():
    usuario = Usuario.query.get(request.usuario_id)
    return jsonify(usuario.to_dict())
