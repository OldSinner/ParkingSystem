from Detecting.detector_state import *


class Detector_Stats():
    def __init__(self) -> None:
        self.car_detected = 0
        self.detector_state = DetectorState.SCANNING_FOR_CAR