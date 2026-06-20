import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connection.channel()

channel.queue_declare(
    queue='presencas',
    durable=True
)

def callback(ch, method, properties, body):

    evento = json.loads(body)

    print(evento)

    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )

channel.basic_consume(
    queue='presencas',
    on_message_callback=callback
)

print("Aguardando eventos...")

channel.start_consuming()