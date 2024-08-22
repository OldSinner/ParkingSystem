import json
import traceback
from CarDetector.config.const import APP_NAME
import pika
from .loglevel import LogLevel
from CarDetector import __version__
from ..config.configuration import ConfigManager
from typing import Callable, TypeVar, Any
R = TypeVar('R')
MAX_LEN_STR = 200
LOGS_LEVELS = [LogLevel.INFO, LogLevel.ERROR, LogLevel.WARNING]
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
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(ConfigManager.MQConfiguration.url)
        )
    def LogMethod(self, func: Callable[..., R], *args : Any, **kwargs:Any) -> R:
        method_name = f"{func.__module__}.{func.__name__}"
        _args = self.format_len(args)
        try:
            self.LogInfo(method_name,f"Call:{_args}")
            r = func(*args, **kwargs)
            self.LogInfo(method_name,f"Resp:{self.format_len(r)}")
            return r
        except Exception as ex:
            self.LogErr(method_name,f"Exce:{ex}")
            raise ex

    def format_len(self, args):
        if args is None:
            return "None"
        _args = []
        for arg in args:
            arg_str = str(arg)
            if len(arg_str) > MAX_LEN_STR:
                _args.append(f"{type(arg)}")
            else:
                _args.append(arg_str)
        return _args
        
    
    def LogDebugMethod(self, func: Callable[..., R], *args : Any, **kwargs:Any) -> R:
        method_name = f"{func.__module__}.{func.__name__}"
        try:
            self.LogDbg(method_name,f"Call:{args}")
            r = func(*args, **kwargs)
            self.LogDbg(method_name,f"Resp:({r})")
            return r
        except Exception as ex:
            self.LogErr(method_name,f"Exce:{ex}")
            raise ex
        
    def LogInfo(self, act: str, message: str):
        if LogLevel.INFO not in LOGS_LEVELS:
           return
        self.__Log(1, act, message)

    def LogWarn(self, act: str, message: str):
        if LogLevel.WARNING not in LOGS_LEVELS:
           return
        self.__Log(2, act, message)

    def LogDbg(self, act: str, message: str):
        if LogLevel.DEBUG not in LOGS_LEVELS:
           return
        self.__Log(3, act, message)

    def LogErr(self, act: str, message: str | Exception):
        if LogLevel.ERROR not in LOGS_LEVELS:
           return
        self.__Log(4, act, message)

    def __Log(self, type: int, act: str, message: str | Exception):
        try:
            if(self.connection.is_closed):
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(ConfigManager.MQConfiguration.url)
                    )
            channel = self.connection.channel()
            if isinstance(message, Exception):
                print(traceback.format_exc())
                message = str(message)
            msg = LogMessage(type, act, message)
            channel.basic_publish(
                exchange=ConfigManager.MQConfiguration.logger_exchange,
                routing_key="",
                body=msg.to_json(),
            )
        except TypeError:

            print(msg.to_dict())

Logger = LoggerClass()
