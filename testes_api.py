import requests

BASE_URL = "http://localhost:5200"

EMAIL = "ronald@example.com"
SENHA = "123456"

# 1. Login e obter token
resp = requests.post(f"{BASE_URL}/login", json={"email": EMAIL, "senha": SENHA})
token = resp.json().get("token")
headers = {"Authorization": f"Bearer {token}"}
print("🔐 Token:", token)

# 2. Criar uma nova tarefa
nova_tarefa = {
    "titulo": "Testar via Python",
    "descricao": "Criando tarefa usando requests"
}
resp = requests.post(f"{BASE_URL}/todos", json=nova_tarefa, headers=headers)
print("🆕 Tarefa criada:", resp.json())
tarefa_id = resp.json().get("id")

# 3. Listar todas as tarefas
resp = requests.get(f"{BASE_URL}/todos", headers=headers)
print("📋 Lista de tarefas:", resp.json())

# 4. Atualizar tarefa
atualizacao = {
    "titulo": "Tarefa Atualizada",
    "concluida": True
}
resp = requests.put(f"{BASE_URL}/todos/{tarefa_id}", json=atualizacao, headers=headers)
print("✏️ Tarefa atualizada:", resp.json())

# 5. Obter tarefa específica
resp = requests.get(f"{BASE_URL}/todos/{tarefa_id}", headers=headers)
print("🔍 Tarefa específica:", resp.json())

# 6. Deletar tarefa
resp = requests.delete(f"{BASE_URL}/todos/{tarefa_id}", headers=headers)
print("🗑️ Tarefa deletada. Status:", resp.status_code)

# 7. Confirmar exclusão
resp = requests.get(f"{BASE_URL}/todos", headers=headers)
print("📋 Lista final:", resp.json())
