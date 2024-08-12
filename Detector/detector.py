from ultralytics import YOLO
from const import *
import cv2
class Detector:
    def __init__(self) -> None:
        self.car_model = YOLO(CAR_DETECTOR_MODEL)
        self.license_playe = YOLO(LICENCE_PLATE_MODEL)
        self.cap = cv2.VideoCapture(VIDEO_PATH)
        pass

    def detect(self) -> None:
        ret = True
        while ret:
            ret, frame = self.cap.read()
            frame = cv2.resize(frame,(1280,720))
            cv2.imshow("Frame",frame)
            key = cv2.waitKey(30)
            if key == 27:
                break
            if ret:
                pass