<<<<<<< HEAD
from flask import Blueprint, jsonify, request, current_app
=======
# src/todo_api/auth.py
from flask import Blueprint, request, jsonify
>>>>>>> a30c9bc4ebd28743636eb8a7cde616b52c194906
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from todo_api.routes import token_obrigatorio
from . import db
from .models import Usuario
from src.todo_api.errors import APIError  # Importe a exceção personalizada
import re  # Para validação de email
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

# Expressão regular para validar emails basicamente
EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

def validar_email(email):
    """Valida o formato do email"""
    return bool(EMAIL_REGEX.match(email)) if email else False

@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    """
    Endpoint para registrar um novo usuário.
    ---
    post:
        summary: Registra um novo usuário
        description: >
            Cria um novo usuário na aplicação a partir dos dados fornecidos (nome, email e senha).
            Realiza validações detalhadas dos campos e retorna mensagens de erro apropriadas.
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            nome:
                                type: string
                                example: João Silva
                                description: Nome completo do usuário
                            email:
                                type: string
                                example: joao@email.com
                                description: Email do usuário
                            senha:
                                type: string
                                example: senha1234
                                description: Senha do usuário (mínimo 8 caracteres)
                        required:
                            - nome
                            - email
                            - senha
        responses:
            201:
                description: Usuário registrado com sucesso
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                mensagem:
                                    type: string
                                    example: Usuário registrado com sucesso
                                usuario_id:
                                    type: integer
                                    example: 1
            400:
                description: Dados inválidos ou não fornecidos
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                mensagem:
                                    type: string
                                    example: Dados inválidos
                                erros:
                                    type: object
                                    example: {"email": "Email inválido"}
            409:
                description: Email já registrado
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                mensagem:
                                    type: string
                                    example: Email já registrado
            500:
                description: Erro interno ao registrar usuário
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                mensagem:
                                    type: string
                                    example: Erro ao registrar usuário
    """
    '''Endpoint para registrar um novo usuário'''
    data = request.json
<<<<<<< HEAD
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
=======
    
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
    """
    Autentica um usuário e retorna um token de acesso JWT.
    ---
    post:
        summary: Autenticação de usuário
        description: Realiza o login de um usuário com email e senha, retornando um token JWT para autenticação nas próximas requisições.
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            email:
                                type: string
                                example: usuario@email.com
                            senha:
                                type: string
                                example: senha123
        responses:
            200:
                description: Login bem-sucedido
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                mensagem:
                                    type: string
                                    example: Login bem-sucedido
                                usuario_id:
                                    type: integer
                                    example: 1
                                nome:
                                    type: string
                                    example: João Silva
                                token:
                                    type: string
                                    example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
            400:
                description: Dados não fornecidos ou inválidos
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                mensagem:
                                    type: string
                                    example: Email e senha são obrigatórios
            401:
                description: Credenciais inválidas
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                mensagem:
                                    type: string
                                    example: Credenciais inválidas
    """
    
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

    token_acesso = create_access_token(identity=str(usuario.id))

    # Login bem sucedido
    return jsonify({
        "mensagem": "Login bem-sucedido",
        "usuario_id": usuario.id,
        "nome": usuario.nome,
        "token": token_acesso
    }), 200


# src/auth.py (adicionar temporariamente)
@auth_bp.route('/usuarios', methods=['GET'])
def list_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios])
>>>>>>> a30c9bc4ebd28743636eb8a7cde616b52c194906
