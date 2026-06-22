"""
Raspberry Pi - Envio de Presença via RabbitMQ
Método mais robusto e assíncrono para IoT
"""

import pika
import json
from datetime import datetime
import sys
from config import RABBITMQ_HOST, RABBITMQ_QUEUE

def send_attendance_rabbitmq(card_id, nome=None, book_code=None, tipo=None):
    """
    Publica presença no RabbitMQ para o backend processar
    
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
        print(f"[RabbitMQ] Conectando em {RABBITMQ_HOST}...")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(RABBITMQ_HOST, connection_attempts=3, retry_delay=2)
        )
        channel = connection.channel()
        
        # Declarar fila como durable (persiste se servidor cair)
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        
        print(f"[RabbitMQ] Publicando: {payload}")
        
        # Publicar com delivery_mode=2 para persistência
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(payload, ensure_ascii=False),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Mensagem persistente
                content_type='application/json'
            )
        )
        
        print(f"✓ Mensagem publicada na fila '{RABBITMQ_QUEUE}'")
        connection.close()
        return True
        
    except pika.exceptions.AMQPConnectionError:
        print(f"✗ Falha ao conectar em RabbitMQ ({BACKEND_HOST})")
        print("  Verifique se RabbitMQ está rodando na porta 5672")
        return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

if __name__ == "__main__":
    # Exemplos de uso
    
    # Teste 1: Apenas ID
    print("\n=== Teste 1: ID apenas ===")
    send_attendance_rabbitmq("1234567890")
    
    # Teste 2: ID + Nome
    print("\n=== Teste 2: ID + Nome ===")
    send_attendance_rabbitmq("1234567890", "João Silva")
    
    # Teste 3: ID + Nome + Tipo
    print("\n=== Teste 3: ID + Nome + Tipo ===")
    send_attendance_rabbitmq("9876543210", "Maria Santos", tipo="entrada")
    
    # Teste 4: Com livro (biblioteca)
    print("\n=== Teste 4: Com livro ===")
    send_attendance_rabbitmq("1111111111", "Pedro Costa", "LIV001", "retirada")
