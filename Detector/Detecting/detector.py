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
        self.frame_to_detect = {}


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
                    self.scan_for_lp(frame)
                    pass
                case DetectorState.WAITING_FOR_GATE_CLOSE:
                    pass
            self.detector_stats.detector_state = self.state
            cv2draw_stats(frame,self.detector_stats)

            cx1,cy1,cx2,cy2,_ = self.reader.actual_car
            lx1,ly1,lx2,ly2,_,_ = self.reader.actual_lp

            cv2short_rect_pick_car(frame,cx1,cy1,cx2,cy2)
            cv2short_rect_lp(frame,lx1,ly1,lx2,ly2)

            cv2.imshow("CAM"+str(CAM_NUMBER),frame)
            cv2.waitKey(30)
            self.reader.clean()
    def scan_for_lp(self,frame):
        detected, detecions = self.reader.scan_for_car(frame)
        if detected:
            self.reader.find_plates(frame,detecions)
    def prepare_cap(self):
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        width = 1280
        height = 720
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    def scan_for_car(self, frame):
        detected, detecions = self.reader.scan_for_car(frame)
        if detected:
            self.detector_stats.car_detected = len(detecions)
            self.state = DetectorState.PROCESSING_CAR
            for detect in detecions:
                x1,y1,x2,y2, _ = detect
                cv2short_rect_car(frame,x1,y1,x2,y2)
                self.frame_to_detect = frame[int(y1):int(y2),int(x1):int(x2),:]
        else:
            print("NotDetected")
            self.detector_stats.car_detected = len(detecions)
        
    
