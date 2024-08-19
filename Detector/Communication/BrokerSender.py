from Communication.CommunicationModels import ActionRequested
from Communication.Logger import LoggerClass
from Configuration.Configuration import MQConfiguration


import pika


class BrokerSender:
    def __init__(
        self,
        detector,
        config,
        logger,
    ):
        self.config = config
        self.Logger = logger
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.config.url)
        )
        self.detector = detector

    def SendCloseGateSignal(self):
        self._SendGateSignal(2)

    def SendOpenGateSignal(self):
        self._SendGateSignal(1)

    def _SendGateSignal(self, action):
        action_messages = {
            1: "Sending signal to open a gate",
            2: "Sending signal to close a gate",
        }
        self.Logger.LogInfo("BrokerSender.SendGateSignal", action_messages[action])
        channel = self.connection.channel()
        channel.queue_declare(queue=self.config.gate_action_queue)
        signal = ActionRequested(action)
        channel.basic_publish(
            exchange="",
            routing_key=self.config.gate_action_queue,
            body=signal.to_json(),
        )
