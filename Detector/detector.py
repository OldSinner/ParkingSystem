from reader import Reader
from detector_state import DetectorState
from broker import Broker
import cv2
from const import *


class Detector:
    def __init__(self):
        self.state = DetectorState.SCANNING_FOR_CAR
        self.reader = Reader()
        self.broker = Broker()
        self.cap = cv2.VideoCapture(CAM_NUMBER)


    def run(self):
        # Main Loop
        ret = True
        while ret:
            ret, frame = self.cap.read()
            
            match self.state:
                case DetectorState.SCANNING_FOR_CAR:
                    self.scan_for_car(frame)
                case DetectorState.PROCESSING_CAR:
                    pass
                case DetectorState.WAITING_FOR_DESAPEAR_CAR:
                    pass
            cv2.imshow("CAM"+str(CAM_NUMBER),frame)
            cv2.waitKey(30)
            

    def scan_for_car(self, frame):
        detected, detecions = self.reader.scan_for_car(frame)
        if detected:
            print("Detected")
        else:
            print("NotDetected")

    
