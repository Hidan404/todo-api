# src/todo_api/config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///todos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Adicione outras configurações (SECRET_KEY, etc.)