from Detecting.Reader import Reader
from enum import Enum
from Helpers.cv2short import *
from Helpers.const import *
from datetime import datetime
from Communication.Broker import *
import cv2
import os 
import threading
class Detector:
    def __init__(self):
        self.state = DetectorState.SCANNING_FOR_CAR
        self.stats = DetectorStats()
        # Reading
        self.reader = Reader()
        self.frame_without_car = 0
        # Comunication
        self.BrokerSender = BrokerSender(self)
        self.BrokerReceiver = BrokerReceiver(self)
        self.RunBrokers()
        # Prepare Cap
        cap = cv2.VideoCapture(CAM_NUMBER)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
        self.cap = cap
    def __enter__(self):
        return self;
    def __exit__(self, exc_type, exc_value, traceback):
        self.BrokerReceiver.Disspose()
        pass
    def RunBrokers(self):
        threading.Thread(target=self.BrokerReceiver.Consume, daemon=True).start()

    def Run(self):
        # Main Loop
        while True:
            _, frame = self.cap.read()
            match self.state:
                case DetectorState.SCANNING_FOR_CAR:
                    self.ScanCar(frame)
                case DetectorState.PROCESSING_CAR:
                    self.ScanLP(frame)
                    pass
                case DetectorState.WAITING_FOR_GATE_CLOSE:
                    pass
                case DetectorState.WAITING_FOR_GATE_OPEN:
                    pass
            self.stats.DetectorState = self.state

            self.DrawDetecionRegions(frame)
            cv2.imshow("CAM"+str(CAM_NUMBER),frame)
            self.reader.Clean()
            key = cv2.waitKey(60)
            if key == 27:
                break

    def DrawDetecionRegions(self, frame):

        cv2draw_stats(frame,self.stats)
        cx1,cy1,cx2,cy2,_ = self.reader.actual_car
        lx1,ly1,lx2,ly2,_,_ = self.reader.actual_lp
        cv2short_rect_pick_car(frame,cx1,cy1,cx2,cy2)
        cv2short_rect_lp(frame,lx1,ly1,lx2,ly2)

    def ScanLP(self,frame):
        detected, detecions = self.ScanCar(frame)
        if detected:
            self.frame_without_car = 0
            res, text = self.reader.FindPlate(frame,detecions)
            if res == -1:
                self.ProcessCarAndLP(frame, text)
        else:
            self.frame_without_car += 1
            if self.frame_without_car > FRAME_WITHOUT_CAR:
                self.state = DetectorState.SCANNING_FOR_CAR

    def ProcessCarAndLP(self, frame, text):
        if self.stats.GateStatus == GateState.OPEN:
            self.state = DetectorState.WAITING_FOR_GATE_CLOSE
        else:
            self.state = DetectorState.WAITING_FOR_GATE_OPEN

        self.stats.ActualLp = text
        self.SaveFiles(frame,text,self.reader.actual_lp,self.reader.actual_car)

    def ScanCar(self, frame):
        detected, detecions = self.reader.ScanForCar(frame)
        if detected:
            self.stats.CarCount = len(detecions)
            self.state = DetectorState.PROCESSING_CAR
            return (detected,detecions)
        else:
            self.stats.CarCount = len(detecions)
            return (False,[])

    def SaveFiles(self,frame,lp_number,lp,car) -> None:

        current_date = datetime.now().strftime("%m%d%YT%H%M%S")
        folder_name = f"{lp_number}_{current_date}"
        path = os.path.join(PATH_TO_FILE,folder_name)
        os.makedirs(path,exist_ok=True)

        filepath_c = os.path.join(path,f"Car_{lp_number}.jpg")
        filepath_lp = os.path.join(path,f"LP_{lp_number}.jpg")
        # 
        cx1,cy1,cx2,cy2,_ = car
        x1, y1, x2, y2, score, _ = lp
        
        lp_crop = frame[int(y1):int(y2),int(x1):int(x2),:]
        car_Crop = frame[int(cy1):int(cy2),int(cx1):int(cx2),:]
        cv2.imwrite(filepath_c,car_Crop)
        cv2.imwrite(filepath_lp,lp_crop)

        self.BrokerSender.SendOpenGateSignal()
    


class DetectorStats():
    def __init__(self) -> None:
        self.CarCount = 0
        self.DetectorState = DetectorState.SCANNING_FOR_CAR
        self.ActualLp = ""
        self.GateStatus = GateState.CLOSED

class DetectorState(Enum):
    SCANNING_FOR_CAR = 1
    PROCESSING_CAR = 2
    WAITING_FOR_GATE_OPEN = 3
    WAITING_FOR_GATE_CLOSE = 4

class GateState(Enum):
    OPEN = 1,
    CLOSED = 2

    

    

          
        
    
