from Detecting.reader import Reader
from Detecting.detector_state import DetectorState
from Detecting.detector_stats import *
from Helpers.cv2short import *
from Communication.broker import Broker, BrokerConsumer
from Helpers.const import *
from datetime import datetime
import cv2
import os 
import threading
class Detector:
    def __init__(self):
        self.state = DetectorState.SCANNING_FOR_CAR
        self.reader = Reader()
        self.broker = Broker(self)
        self.consumer = BrokerConsumer(self)
        self.cap = cv2.VideoCapture(CAM_NUMBER)
        self.detector_stats = Detector_Stats()
        self.frame_to_detect = {}
        self.frame_without_car = 0
        threading.Thread(target=self.consumer.consume_messages, daemon=True).start()

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.broker.disspose()
        self.consumer.disspose()
        pass
    
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
            cv2.waitKey(60    )
            self.reader.clean()

    def scan_for_lp(self,frame):
        detected, detecions = self.reader.scan_for_car(frame)
        if detected:
            self.frame_without_car = 0
            res, text = self.reader.find_plates(frame,detecions)
            if res == -1:
                self.state = DetectorState.WAITING_FOR_GATE_CLOSE
                self.detector_stats.detected_lp = text
                self.save_photos(frame,text,self.reader.actual_lp,self.reader.actual_car)
        else:
            self.frame_without_car += 1
            if self.frame_without_car > FRAME_WITHOUT_CAR:
                self.state = DetectorState.SCANNING_FOR_CAR
    def prepare_cap(self):
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        width = 1280
        height = 720
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def save_photos(self,frame,lp_number,lp,car) -> None:
        current_date = datetime.now().strftime("%m%d%YT%H%M%S")
        folder_name = f"{lp_number}_{current_date}"
        path = os.path.join(PATH_TO_FILE,folder_name)
        os.makedirs(path,exist_ok=True)
        filepath_c = os.path.join(path,f"Car_{lp_number}.jpg")
        filepath_lp = os.path.join(path,f"LP_{lp_number}.jpg")
        self.broker.SendLP(lp_number,folder_name)
        # 
        cx1,cy1,cx2,cy2,_ = car
        x1, y1, x2, y2, score, _ = lp
        lp_crop = frame[int(y1):int(y2),int(x1):int(x2),:]
        car_Crop = frame[int(cy1):int(cy2),int(cx1):int(cx2),:]
        cv2.imwrite(filepath_c,car_Crop)
        cv2.imwrite(filepath_lp,lp_crop)
    

    def scan_for_car(self, frame):
        detected, detecions = self.reader.scan_for_car(frame)
        if detected:
            self.detector_stats.car_detected = len(detecions)
            self.state = DetectorState.PROCESSING_CAR
            for detect in detecions:
                x1,y1,x2,y2, _ = detect
                cv2short_rect_car(frame,x1,y1,x2,y2)
        else:
            self.detector_stats.car_detected = len(detecions)

    def gate_closed(self):
        self.state = DetectorState.SCANNING_FOR_CAR
        self.detector_stats = Detector_Stats()
          
        
    
