from .detector import Detector
from ..logger import LoggerClass
from ..config import Configuration
class Wrapper:
    def __init__(self):
        self._logger : LoggerClass = LoggerClass()
        self.detector : Detector = Detector(self._logger)
    def run(self):
        self.detector.run()