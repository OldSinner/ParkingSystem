from Detecting.reader import Reader
from Detecting.detector_state import DetectorState
from Detecting.detector_stats import *
from Helpers.cv2short import *
from Communication.broker import Broker
import cv2
from Helpers.const import *


class Detector:
    def __init__(self):
        self.state = DetectorState.SCANNING_FOR_CAR
        self.reader = Reader()
        self.broker = Broker()
        self.cap = cv2.VideoCapture(CAM_NUMBER)
        self.detector_stats = Detector_Stats()


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
                case DetectorState.WAITING_FOR_GATE_CLOSE:
                    pass
            self.detector_stats.detector_state = self.state
            cv2draw_stats(frame,self.detector_stats)
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
            self.detector_stats.car_detected = len(detecions)
        else:
            print("NotDetected")
            self.detector_stats.car_detected = len(detecions)
        
    
