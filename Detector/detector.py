from reader import Reader
from detector_state import DetectorState
from broker import Broker
class Detector:
    def __init__(self):
        self.state = DetectorState.SCANNING_FOR_CAR
        self.reader = Reader()
        self.broker = Broker()

    def run(self):
        # Main Loop
        while True:
            match self.state:
                case DetectorState.SCANNING_FOR_CAR:
                    self.scan_for_car()
                case DetectorState.PROCESSING_CAR:
                    pass
                case DetectorState.WAITING_FOR_DESAPEAR_CAR:
                    pass

    def scan_for_car(self):
        pass               

    
