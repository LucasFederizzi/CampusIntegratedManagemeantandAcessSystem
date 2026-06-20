import serial
import json

from producer import enviar_evento
from datetime import datetime

arduino = serial.Serial(
    '/dev/ttyACM0',
    9600,
    timeout=1
)

LOCAL = "SALA_101"

print("Aguardando cartões...")

while True:

    linha = arduino.readline().decode().strip()

    if not linha:
        continue

    try:

        dados = json.loads(linha)

        # Ignora mensagens que não são RFID
        if dados.get("evento") != "rfid":
            continue

        uid = dados["uid"]

        evento = {
            "uid": uid,
            "timestamp": datetime.now().isoformat(),
            "local": LOCAL,
            "tipo": "presenca"
        }

        # ENVIA PARA O RABBITMQ
        enviar_evento(evento)

        print("Evento enviado:")
        print(evento)

    except Exception as e:

        print("Erro ao processar mensagem:")
        print(linha)
        print(e)