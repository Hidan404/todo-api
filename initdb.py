import sys
import os
from pathlib import Path

# Configura caminhos absolutos
BASE_DIR = Path(__file__).parent
SRC_DIR = BASE_DIR / 'src'

# Adiciona src ao PYTHONPATH
sys.path.insert(0, str(SRC_DIR))

# Importa após ajustar o PATH
from todo_api import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tabelas criadas com sucesso!")
    
    # Listar tabelas criadas
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    print(f"Tabelas: {inspector.get_table_names()}")