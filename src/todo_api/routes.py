from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

banco_de_dados = SQLAlchemy()


class Usuario(banco_de_dados.Model):
    __tablename__ = 'usuarios'
    id = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    nome = banco_de_dados.Column(banco_de_dados.String(50), nullable=False)
    email = banco_de_dados.Column(banco_de_dados.String(120), unique=True, nullable=False)
    senha = banco_de_dados.Column(banco_de_dados.String(128), nullable=False)
    data_criacao = banco_de_dados.Column(banco_de_dados.DateTime, default=datetime.utcnow)

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
class Tarefa(banco_de_dados.Model):
    __tablename__ = 'tarefas'
    id = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    titulo = banco_de_dados.Column(banco_de_dados.String(100), nullable=False)
    descricao = banco_de_dados.Column(banco_de_dados.String(500), nullable=True)
    concluida = banco_de_dados.Column(banco_de_dados.Boolean, default=False)
    data_criacao = banco_de_dados.Column(banco_de_dados.DateTime, default=datetime.utcnow)
    usuario_id = banco_de_dados.Column(banco_de_dados.Integer, banco_de_dados.ForeignKey('usuarios.id'), nullable=False)

    usuario = banco_de_dados.relationship('Usuario', backref=banco_de_dados.backref('tarefas', lazy=True))    