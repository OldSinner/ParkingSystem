import pika
from Communication.CommunicationModels import *
from Communication.ActionHandler import *
from Helpers.const import *
from Configuration.Configuration import *


class BrokerReceiver:
    def __init__(self, detector, config: MQConfiguration):
        self.detector = detector
        self.actionHandler = ActionHandler(detector)
        self.config = config
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.config.url)
        )

    def Dispose(self):
        self.connection.close()

    def callback(self, ch, method, properties, body):
        response = GateEvent(body)
        self.actionHandler.MakeActionOnEvent(response)

    def Consume(self):
        channel = self.connection.channel()
        channel.exchange_declare(
            exchange=self.config.gate_event_queue, exchange_type="fanout"
        )
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=self.config.gate_event_queue, queue=queue_name)
        channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True
        )
        channel.start_consuming()


class BrokerSender:
    def __init__(self, detector, config: MQConfiguration):
        self.config = config
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.config.url)
        )
        self.detector = detector

    def SendCloseGateSignal(self):
        self.SendGateSignal(2)

    def SendOpenGateSignal(self):
        self.SendGateSignal(1)

    def SendGateSignal(self, action):
        channel = self.connection.channel()
        channel.queue_declare(queue=self.config.gate_action_queue)
        signal = ActionRequested(action)
        channel.basic_publish(
            exchange="",
            routing_key=self.config.gate_action_queue322,
            body=signal.to_json(),
        )
