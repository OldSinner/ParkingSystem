import pika
class Broker:
    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = self.connection.channel()
        channel.queue_declare(queue='LP_CODES')
        pass
    def disspose(self) -> None:
        self.connection.close()