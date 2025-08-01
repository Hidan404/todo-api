from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_obrigatorio(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'erro': 'Token ausente'}), 401

        if not auth_header.startswith('Bearer '):
            return jsonify({'erro': 'Formato do token inválido'}), 401

        token = auth_header.split(' ')[1]  # pega apenas o token

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            request.usuario_id = payload['usuario_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401

        return f(*args, **kwargs)
    return decorator
