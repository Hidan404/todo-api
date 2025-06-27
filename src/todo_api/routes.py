from flask import Blueprint
from . import db
from .models import Tarefa  # Nome correto do modelo

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todos')
def get_todos():
    todos = Tarefa.query.all()
    return {"todos": [todo.to_dict() for todo in todos]}