# test_db.py
from src.todo_api import create_app, db
from src.todo_api.models import Usuario

app = create_app()

with app.app_context():
    # Criar usuário de teste
    db.drop_all()  # Limpar o banco de dados antes de criar as tabelas
    db.create_all()  # Criar as tabelas
    novo_usuario = Usuario(nome="Teste", email="teste@example.com", senha="123456")
    db.session.add(novo_usuario)
    db.session.commit()
    
    # Consultar usuários
    usuarios = Usuario.query.all()
    print(f"Usuários no banco: {len(usuarios)}")
    
    # Verificar tabelas
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    print(f"Tabelas: {inspector.get_table_names()}")