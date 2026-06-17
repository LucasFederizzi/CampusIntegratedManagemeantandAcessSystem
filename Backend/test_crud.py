"""
Script de teste para todos os endpoints CRUD
Execute: python test_crud.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api/presenca"

def test_create():
    print("\n=== CREATE: Registrar presença ===")
    payload = {
        "id": "1234567890",
        "nome": "João Silva",
        "hora": "2026-06-16 14:30:00"
    }
    response = requests.post(BASE_URL, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get("pk")

def test_read_all():
    print("\n=== READ: Listar todas as presenças ===")
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total de registros: {len(data)}")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return data

def test_read_one(pk):
    print(f"\n=== READ: Buscar presença pk={pk} ===")
    response = requests.get(f"{BASE_URL}/{pk}")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_update(pk):
    print(f"\n=== UPDATE: Atualizar presença pk={pk} ===")
    payload = {
        "nome": "João Silva Atualizado",
        "hora": "2026-06-16 15:45:00"
    }
    response = requests.put(f"{BASE_URL}/{pk}", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_delete(pk):
    print(f"\n=== DELETE: Deletar presença pk={pk} ===")
    response = requests.delete(f"{BASE_URL}/{pk}")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    try:
        # 1. Criar
        pk = test_create()
        
        # 2. Listar todas
        test_read_all()
        
        # 3. Buscar uma
        test_read_one(pk)
        
        # 4. Atualizar
        test_update(pk)
        
        # 5. Listar novamente para confirmar atualização
        test_read_one(pk)
        
        # 6. Deletar
        test_delete(pk)
        
        # 7. Confirmar deleção
        print("\n=== Confirmando deleção ===")
        response = requests.get(f"{BASE_URL}/{pk}")
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Erro: {e}")
        print("Certifique-se de que o backend está rodando em http://127.0.0.1:5000")
