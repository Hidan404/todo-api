from src.todo_api import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5100)  # Configurar para rodar na porta 5100