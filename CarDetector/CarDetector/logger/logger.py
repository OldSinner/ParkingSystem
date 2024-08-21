import json
import traceback
from CarDetector.config.const import APP_NAME
import pika
from ..config import  MQConfiguration
from CarDetector import __version__
class LogMessage:
    def __init__(self, LogType: int, Action: str, Message: str) -> None:
        self.LogType = LogType
        self.Action = Action
        self.Message = Message
        self.Service = APP_NAME
        self.Version = str(__version__)

    def to_dict(self):
        return {
            attr: getattr(self, attr)
            for attr in ["LogType", "Action", "Message", "Service", "Version"]
        }

    def to_json(self):
        return json.dumps(self.to_dict())

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

    def LogErr(self, act: str, message: str | Exception):
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
