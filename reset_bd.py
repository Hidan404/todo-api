# reset_db.py
from src.todo_api import create_app, db

app = create_app()

with app.app_context():
    print("Apagando banco de dados...")
    db.drop_all()
    print("Criando novas tabelas...")
    db.create_all()
    print("Banco resetado com sucesso!")