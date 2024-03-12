import time
import json

import pika

from models import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.queue_declare(queue='email', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    message = body.decode()
    contact = Contact.objects(id=message)
    print(f" [x] Sent email to {contact[0].email}")
    contact[0].update(msg_sent=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email', on_message_callback=callback)


if __name__ == '__main__':
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')