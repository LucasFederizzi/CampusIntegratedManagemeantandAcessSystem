# Conexão Raspberry Pi + Arduino + RFID

## ⚙️ Configuração de IP

Abra o arquivo `config.py` e edite:

```python
# IP ou hostname do Backend (onde app.py está rodando)
BACKEND_HOST = "192.168.1.100"  # ← ALTERE PARA SEU IP
BACKEND_PORT = 5000

# RabbitMQ
RABBITMQ_HOST = "192.168.1.100"  # ← ALTERE PARA SEU IP
RABBITMQ_PORT = 5672

# Serial (Arduino)
SERIAL_PORT = "/dev/ttyUSB0"  # ← Altere conforme necessário
SERIAL_BAUD_RATE = 9600
```

### Como descobrir o IP do Backend

1. **No computador que está rodando o backend:**
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig` ou `hostname -I`

2. **Procure por:**
   - `IPv4 Address` ou
   - `inet` (exclua 127.0.0.1)

3. **Exemplo:**
   ```
   IPv4 Address . . . . . . . . . . : 192.168.1.50
   ```

### SERIAL_PORT por SO

- **Linux**: `/dev/ttyUSB0` ou `/dev/ttyACM0`
- **Windows**: `COM3`, `COM4`, etc
- **Raspberry Pi**: `/dev/ttyUSB0` (Arduino conectado)

## Arquitetura

```
Raspberry Pi (RFID Reader) 
    ↓
    ├─→ HTTP POST → Backend (Port 5000) → SQLite
    └─→ RabbitMQ Publish → Backend (Consumer) → SQLite
```

O backend processa automaticamente de ambas as formas.

## Opção 1: HTTP POST (Simples)

### Raspberry Pi Code

```python
import requests
import json
from datetime import datetime

BACKEND_URL = "http://192.168.1.100:5000/api/presenca"  # IP do Backend

def send_attendance(card_id, nome):
    """Envia presença via HTTP POST"""
    payload = {
        "id": card_id,
        "nome": nome,
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "book_code": "LIV001",  # Opcional
        "tipo": "entrada"  # Opcional
    }
    
    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=5)
        if response.status_code == 201:
            print(f"✓ Presença registrada: {response.json()}")
        else:
            print(f"✗ Erro: {response.text}")
    except Exception as e:
        print(f"✗ Falha ao conectar: {e}")

# Exemplo de uso com RFID
if __name__ == "__main__":
    # Simular leitura de RFID
    card_id = "1234567890"
    nome = "João Silva"
    
    send_attendance(card_id, nome)
```

## Opção 2: RabbitMQ (Recomendado para IoT)

### Raspberry Pi Code

```python
import pika
import json
from datetime import datetime

def send_attendance_rabbitmq(card_id, nome):
    """Publica presença no RabbitMQ"""
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('192.168.1.100')  # IP do Backend
        )
        channel = connection.channel()
        channel.queue_declare(queue='presencas', durable=True)
        
        payload = {
            "id": card_id,
            "nome": nome,
            "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "book_code": "LIV001",  # Opcional
            "tipo": "entrada"  # Opcional
        }
        
        channel.basic_publish(
            exchange='',
            routing_key='presencas',
            body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=2)  # persistent
        )
        
        print(f"✓ Mensagem publicada: {payload}")
        connection.close()
    except Exception as e:
        print(f"✗ Erro RabbitMQ: {e}")

if __name__ == "__main__":
    card_id = "1234567890"
    nome = "João Silva"
    
    send_attendance_rabbitmq(card_id, nome)
```

## Instalação na Raspberry Pi

```bash
# Para HTTP
pip install requests

# Para RabbitMQ
pip install pika

# Para ambos
pip install -r requirements.txt
```

## Exemplo com Arduino + RFID (Serial)

```python
import serial
import requests
from datetime import datetime

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600
BACKEND_URL = "http://192.168.1.100:5000/api/presencia"

def read_rfid_and_send():
    """Lê RFID via serial e envia ao backend"""
    try:
        serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("Aguardando leitura RFID...")
        
        while True:
            if serial_connection.in_waiting > 0:
                rfid_data = serial_connection.readline().decode().strip()
                
                if rfid_data:
                    card_id = rfid_data
                    payload = {
                        "id": card_id,
                        "nome": "Usuário RFID",
                        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    try:
                        response = requests.post(BACKEND_URL, json=payload, timeout=5)
                        print(f"✓ Registrado: {card_id}")
                    except Exception as e:
                        print(f"✗ Erro: {e}")
    
    except Exception as e:
        print(f"Erro de conexão serial: {e}")

if __name__ == "__main__":
    read_rfid_and_send()
```

## Processamento de Dados

Quando a Raspberry enviar dados:

### Via HTTP POST
1. Requisição chega em `POST /api/presenca`
2. Backend valida payload
3. Função `insert_presenca_from_payload()` salva no SQLite
4. Resposta HTTP com status 201

### Via RabbitMQ
1. Mensagem publicada na fila `presencas`
2. Consumer (thread background) recebe
3. Mesmo `insert_presenca_from_payload()` valida e salva
4. Sem resposta HTTP (async)

Ambos salvam no mesmo banco de dados!

## Verificar se está funcionando

```bash
# Ver registros via API
curl http://192.168.1.100:5000/api/presenca

# Ou abrir no navegador
http://192.168.1.100:8000  # Frontend
```

## Notas

- **Configure o IP em `config.py`** antes de rodar qualquer script
- HTTP é mais simples, RabbitMQ é mais robusto
- Dados são processados automaticamente após conexão
- Use `python -m serial.tools.list_ports` para descobrir a porta serial
