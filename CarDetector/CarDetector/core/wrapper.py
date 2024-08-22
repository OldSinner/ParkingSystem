from .detector import DetectorLog
from ..config import Configuration
class Wrapper:
    def __init__(self):
        self.detector : DetectorLog = DetectorLog()
    def run(self):
        self.detector.run()