# src/todo_api/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Usuario
from src.todo_api.errors import APIError  # Importe a exceção personalizada
import re  # Para validação de email

auth_bp = Blueprint('auth', __name__)

# Expressão regular para validação básica de email
EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

def validar_email(email):
    """Valida o formato do email"""
    return bool(EMAIL_REGEX.match(email)) if email else False

@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.json
    
    # Verifica se os dados foram fornecidos
    if not data:
        raise APIError("Dados não fornecidos", 400)
    
    # Extrai e valida campos
    email = data.get('email', '').strip()
    senha = data.get('senha', '').strip()
    nome = data.get('nome', '').strip()
    
    # Validação detalhada
    erros = {}
    if not email:
        erros['email'] = "Email é obrigatório"
    elif not validar_email(email):
        erros['email'] = "Email inválido"
    
    if not senha:
        erros['senha'] = "Senha é obrigatória"
    elif len(senha) < 8:
        erros['senha'] = "Senha deve ter pelo menos 8 caracteres"
    
    if not nome:
        erros['nome'] = "Nome é obrigatório"
    
    if erros:
        raise APIError("Dados inválidos", 400, payload={"erros": erros})
    
    # Verifica se o email já existe
    if Usuario.query.filter_by(email=email).first():
        raise APIError("Email já registrado", 409)
    
    # Cria o novo usuário
    novo_usuario = Usuario(
        nome=nome, 
        email=email,
    )
    novo_usuario.set_senha(senha)
    
    try:
        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify({
            "mensagem": "Usuário registrado com sucesso",
            "usuario_id": novo_usuario.id
        }), 201
    except Exception as e:
        db.session.rollback()
        raise APIError("Erro ao registrar usuário", 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    
    # Verifica se os dados foram fornecidos
    if not data:
        raise APIError("Dados não fornecidos", 400)
    
    email = data.get('email', '').strip()
    senha = data.get('senha', '').strip()
    
    # Validação básica
    if not email or not senha:
        raise APIError("Email e senha são obrigatórios", 400)
    
    # Busca o usuário
    usuario = Usuario.query.filter_by(email=email).first()
    
    # Verifica credenciais
    if not usuario:
        raise APIError("Credenciais inválidas", 401)
    
    if not usuario.verificar_senha(senha):
        raise APIError("Credenciais inválidas", 401)
    
    # Login bem sucedido
    return jsonify({
        "mensagem": "Login bem-sucedido",
        "usuario_id": usuario.id,
        "nome": usuario.nome
    }), 200


# src/auth.py (adicionar temporariamente)
@auth_bp.route('/usuarios', methods=['GET'])
def list_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios])