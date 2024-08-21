from .detector import Detector
from ..logger import LoggerClass
from ..config import Configuration
class Wrapper:
    def __init__(self):
        _config : Configuration = Configuration()
        self._logger : LoggerClass = LoggerClass(_config.MQConfiguration)
        self.detector : Detector = Detector(self._logger,_config)
    def run(self):
        self.detector.run()