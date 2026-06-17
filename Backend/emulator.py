import sys
from datetime import datetime
import requests


API_URL = "http://127.0.0.1:5000/api/presenca"


def enviar_presenca(card_id: str, nome: str, hora: str = None):
    hora = hora or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {"id": card_id, "nome": nome, "hora": hora}
    response = requests.post(API_URL, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    card_id = sys.argv[1] if len(sys.argv) > 1 else "1234567890"
    nome = sys.argv[2] if len(sys.argv) > 2 else "Aluno Exemplo"
    hora = sys.argv[3] if len(sys.argv) > 3 else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    resultado = enviar_presenca(card_id, nome, hora)
    print(resultado)
