from ultralytics import YOLO
from const import *
class Detector:
    def __init__(self) -> None:
        self.car_model = YOLO(CAR_DETECTOR_MODEL)
        self.license_playe = YOLO(LICENCE_PLATE_MODEL)
        pass

    def loadModels(self) -> None:
        pass