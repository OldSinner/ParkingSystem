import pika
from Communication.CommunicationModels import *
from Communication.ActionHandler import *
from Helpers.const import *
class BrokerReceiver:
    def __init__(self, detector):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_URL))
        self.detector = detector
        self.actionHandler = ActionHandler(detector)
    def Disspose(self):
        self.connection.close()

    def callback(self,ch, method, properties, body):
        response = GateEvent(body)
        self.actionHandler.MakeActionOnEvent(response)

    def Consume(self):
        channel = self.connection.channel()
        channel.queue_declare(queue=GATE_EVENT_QUEUE)
        channel.basic_consume(queue=GATE_EVENT_QUEUE, on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()

class BrokerSender:
    def __init__(self, detector):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_URL))
        self.detector = detector
    def SendCloseGateSignal(self):
        self.SendGateSignal(2)
    def SendOpenGateSignal(self):
        self.SendGateSignal(1)
    def SendGateSignal(self, action):
        channel = self.connection.channel()
        channel.queue_declare(queue=GATE_ACTION_QUEUE)
        signal = ActionRequested(action)
        channel.basic_publish(exchange='',
                      routing_key=GATE_ACTION_QUEUE,
                      body=signal.to_json())
        
        


