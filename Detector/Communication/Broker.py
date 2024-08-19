import pika
from Communication.CommunicationModels import *
from Communication.Logger import LoggerClass
from Helpers.const import *
from Configuration.Configuration import *


class BrokerReceiver:
    def __init__(self, detector, config: MQConfiguration, logger: LoggerClass):
        self.detector = detector
        self.config = config
        self.Logger = logger
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.config.url)
        )

    def Dispose(self):
        self.connection.close()

    def callback(self, ch, method, properties, body):
        response = GateEvent(body)
        print(response)

    def Consume(self):
        try:
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
            self.Logger.LogInfo("BrokerReceiver.Consume", "start_consuming")
            channel.start_consuming()
        except Exception as ex:
            self.Logger.LogErr("BrokerReceiver.Consume", ex)


class BrokerSender:
    def __init__(self, detector, config: MQConfiguration, logger: LoggerClass):
        self.config = config
        self.Logger = logger
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.config.url)
        )
        self.detector = detector

    def SendCloseGateSignal(self):
        self.Logger.LogInfo(
            "BrokerSender.SendOpenGateSignal", "Sending signal to close a gate"
        )

        self.SendGateSignal(2)

    def SendOpenGateSignal(self):
        self.Logger.LogInfo(
            "BrokerSender.SendOpenGateSignal", "Sending signal to open a gate"
        )
        self.SendGateSignal(1)

    def SendGateSignal(self, action):
        channel = self.connection.channel()
        channel.queue_declare(queue=self.config.gate_action_queue)
        signal = ActionRequested(action)
        channel.basic_publish(
            exchange="",
            routing_key=self.config.gate_action_queue,
            body=signal.to_json(),
        )
