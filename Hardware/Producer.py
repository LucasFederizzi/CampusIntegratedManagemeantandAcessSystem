import json
import pika

RABBIT_HOST = "192.168.1.100"  # servidor

def enviar_evento(evento):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(RABBIT_HOST)
    )

    channel = connection.channel()

    channel.queue_declare(
        queue='presencas',
        durable=True
    )

    channel.basic_publish(
        exchange='',
        routing_key='presencas',
        body=json.dumps(evento),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()