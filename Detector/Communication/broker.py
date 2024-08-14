import pika
import json
from datetime import datetime
from Detecting.detector_state import *
class Broker:
    def __init__(self, parent) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.parent  = parent
        pass
    def disspose(self) -> None:
        self.connection.close()
    
    def SendLP(self, lp_code, path) -> None:
        channel = self.connection.channel()
        channel.queue_declare(queue='LP_CODES')
        obj = {
            "LP_CODE":lp_code,
            "PATH":path,
            "Time":datetime.now().strftime("%m/%d/%YT%H:%M:%S")
        }
        channel.basic_publish(exchange='',
                      routing_key='LP_CODES',
                      body=json.dumps(obj))

class BrokerConsumer:
    def __init__(self, parent) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.parent  = parent
        pass
    def disspose(self) -> None:
        self.connection.close()
    def consume_callback(self, ch, method, properties, body):
        self.parent.gate_closed()
        print(f" [x] Received {body}")
    def consume_messages(self):
        channel = self.connection.channel()
        channel.queue_declare(queue='GATE_ACTION_CLOSED')
        channel.basic_consume(queue='GATE_ACTION_CLOSED', on_message_callback=self.consume_callback, auto_ack=True)
        channel.start_consuming()    