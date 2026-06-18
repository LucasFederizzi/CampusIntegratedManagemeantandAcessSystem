import json
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('IP_DO_SERVIDOR')
)

channel = connection.channel()

channel.queue_declare(
    queue='presencas',
    durable=True
)

evento = {
    "uid": "A1B2C3D4",
    "timestamp": "2025-06-18T20:30:00",
    "local": "SALA_101"
}

channel.basic_publish(
    exchange='',
    routing_key='presencas',
    body=json.dumps(evento),
    properties=pika.BasicProperties(
        delivery_mode=2
    )
)

print("Evento enviado")

connection.close()