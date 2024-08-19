import pika
from enum import Enum
from Configuration.Configuration import *
from Communication.CommunicationModels import *


class LoggerClass:
    def __init__(self, config: MQConfiguration):
        self.config = config
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.config.url)
        )

    def LogInfo(self, act: str, message: str):
        self.Log(1, act, message)

    def LogWarn(self, act: str, message: str):
        self.Log(2, act, message)

    def LogDbg(self, act: str, message: str):
        self.Log(3, act, message)

    def LogErr(self, act: str, message: str):
        self.Log(4, act, message)

    def Log(self, type: int, act: str, message: str):
        channel = self.connection.channel()
        msg = LogMessage(type, act, message)
        channel.basic_publish(
            exchange=self.config.logger_exchange,
            routing_key="",
            body=msg.to_json(),
        )
