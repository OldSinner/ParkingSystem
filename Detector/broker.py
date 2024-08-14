import pika
class Broker:
    def __init__(self) -> None:
        pass

    def TestConnect(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
        connection.close()