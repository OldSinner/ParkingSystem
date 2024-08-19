import traceback
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
        self.__Log(1, act, message)

    def LogWarn(self, act: str, message: str):
        self.__Log(2, act, message)

    def LogDbg(self, act: str, message: str):
        self.__Log(3, act, message)

    def LogErr(self, act: str, message: str):
        self.__Log(4, act, message)

    def __Log(self, type: int, act: str, message: str | Exception):
        try:
            channel = self.connection.channel()
            if isinstance(message, Exception):
                print(traceback.format_exc())
                message = str(message)
            msg = LogMessage(type, act, message)
            channel.basic_publish(
                exchange=self.config.logger_exchange,
                routing_key="",
                body=msg.to_json(),
            )
        except TypeError:

            print(msg.to_dict())
