# src/todo_api/config.py
import os

# Obter o diretório base do projeto (onde está run.py)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class Config:
    # Apontar para a raiz do projeto
    SECRET_KEY = 'chave-secreta-simples'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              f'sqlite:///{os.path.join(BASE_DIR, "todos.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False