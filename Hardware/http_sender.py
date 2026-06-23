"""
Raspberry Pi - Envio de Presença via HTTP POST
Exemplo simples para conectar RFID ao backend
"""

import requests
import json
from datetime import datetime
import sys
from config import BACKEND_URL, BACKEND_TIMEOUT

def send_attendance(card_id, nome=None, book_code=None, tipo=None):
    """
    Envia presença para o backend via HTTP POST
    
    Args:
        card_id: ID do cartão RFID (obrigatório)
        nome: Nome do usuário (opcional)
        book_code: Código do livro (opcional)
        tipo: Tipo de evento - 'entrada' ou 'saida' (opcional)
    """
    payload = {
        "id": str(card_id),
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if nome:
        payload["nome"] = str(nome)
    if book_code:
        payload["book_code"] = str(book_code)
    if tipo:
        payload["tipo"] = str(tipo)
    
    try:
        print(f"[HTTP] Enviando: {payload}")
        response = requests.post(BACKEND_URL, json=payload, timeout=BACKEND_TIMEOUT)
        
        if response.status_code == 201:
            data = response.json()
            print(f"✓ Sucesso! PK: {data.get('pk')}")
            return True
        else:
            print(f"✗ Erro: Status {response.status_code}")
            print(f"  Resposta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Falha ao conectar em {BACKEND_URL}")
        print("  Verifique se o backend está rodando e o IP está correto")
        return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

if __name__ == "__main__":
    # Exemplos de uso
    
    # Teste 1: Apenas ID
    print("\n=== Teste 1: ID apenas ===")
    send_attendance("1234567890")
    
    # Teste 2: ID + Nome
    print("\n=== Teste 2: ID + Nome ===")
    send_attendance("1234567890", "João Silva")
    
    # Teste 3: ID + Nome + Tipo
    print("\n=== Teste 3: ID + Nome + Tipo ===")
    send_attendance("9876543210", "Maria Santos", tipo="entrada")
    
    # Teste 4: Com livro (biblioteca)
    print("\n=== Teste 4: Com livro ===")
    send_attendance("1111111111", "Pedro Costa", "LIV001", "retirada")
