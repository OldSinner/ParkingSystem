from reader import Reader
from detector_state import DetectorState
from cv2short import *
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
        self.prepare_cap()
        while ret:
            ret, frame = self.cap.read()
            match self.state:
                case DetectorState.SCANNING_FOR_CAR:
                    self.scan_for_car(frame)
                case DetectorState.PROCESSING_CAR:
                    pass
                case DetectorState.WAITING_FOR_DESAPEAR_CAR:
                    pass
            cv2draw_stats(frame,[])
            cv2.imshow("CAM"+str(CAM_NUMBER),frame)
            cv2.waitKey(30)
            
    def prepare_cap(self):
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        width = 1280
        height = 720
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    def scan_for_car(self, frame):
        detected, detecions = self.reader.scan_for_car(frame)
        if detected:
            print("Detected")
        else:
            print("NotDetected")

    
