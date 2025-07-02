from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from .config import Config
from .errors import APIError
from flasgger import Swagger

# Cria a instância única do SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializa a extensão
    db.init_app(app)
    app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta-super-forte'  # Troque por uma chave lembrar
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  # localizção do token esta no cabeçalho
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)  # Expira em 7 dias

    # Configurações recomendadas
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Expira em 1 hora
    app.config['PROPAGATE_EXCEPTIONS'] = True  # Crucial para tratamento de erros
    
  
    # Inicialize o JWTManager
    jwt = JWTManager(app)


    app.config['SWAGGER'] = {
        'title': 'API de Tarefas',
        'uiversion': 3,
        'specs_route': '/docs/',
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
            }
        }
    }
    Swagger(app)

    # Registro de manipuladores de erro
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({
            "success": False,
            "error": "Recurso não encontrado",
            "status_code": 404
        }), 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        app.logger.error(f"Erro interno: {str(error)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "status_code": 500
        }), 500

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        app.logger.exception("Exceção não tratada")
        status_code = getattr(error, 'status_code', 500)
        return handle_api_error(APIError(str(error), status_code))
    
    @app.route('/routes')
    def list_routes():
        return jsonify({
            'routes': [str(rule) for rule in app.url_map.iter_rules()]
        })

    # Importar blueprints DENTRO da função para evitar circularidade
    with app.app_context():
        # Importar modelos primeiro
        from . import models
        
        # Importar blueprints
        from .routes import todo_bp
        from .auth import auth_bp
        
        # Registrar blueprints com prefixos
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(todo_bp, url_prefix='/api')
    
    return app