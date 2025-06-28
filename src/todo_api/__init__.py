from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Cria a instância única do SQLAlchemy
db = SQLAlchemy()

from . import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializa a extensão
    db.init_app(app)
    
    # Importar blueprints DENTRO da função para evitar circularidade
    with app.app_context():
        from .routes import todo_bp
        from .auth import auth_bp
        
        app.register_blueprint(todo_bp)
        app.register_blueprint(auth_bp)
    
    return app

# Importar modelos DEPOIS de criar db para evitar dependência circular
