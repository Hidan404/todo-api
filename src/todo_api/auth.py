# src/todo_api/auth.py
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
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
    
    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    novo_usuario.set_senha(senha)
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({"mensagem": "Usuário registrado com sucesso"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"erro": "Credenciais inválidas"}), 401
    
    return jsonify({"mensagem": "Login bem-sucedido"}), 200