import pika
from Communication.CommunicationModels import *
from Helpers.const import *
class BrokerReceiver:
    def __init__(self, detector):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_URL))
        self.detector = detector
        
    def callback(self,ch, method, properties, body):
        print(f" [x] Received {body}")
        mess = BrokerModel(body)
        print(mess)
    def Disspose(self):
        self.connection.close()
    def Consume(self):
        channel = self.connection.channel()
        channel.queue_declare(queue=APP_NAME)
        channel.basic_consume(queue=APP_NAME, on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()

class BrokerSender:
    def __init__(self, detector):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_URL))
        self.detector = detector
    def SendOpenGateSignal(self):
        channel = self.connection.channel()
        channel.queue_declare(queue=GATE_HANDLER)
        signal = GateSignal(1,"OPEN")
        channel.basic_publish(exchange='',
                      routing_key=GATE_HANDLER,
                      body=signal.to_json())


