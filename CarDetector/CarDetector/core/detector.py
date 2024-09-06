from ..core.scanner import ScannerLog
import cv2
import cv2.mat_wrapper
from ..config import ConfigManager
from ..logger import LoggerMock as Logger
from .scanner import ScannerLog
scanner = ScannerLog()
class DetectorLog:
    def __init__(self):
        self.service = Detector()
    def get_camera_cap(self):
        return Logger.LogMethod(self.service.get_camera_cap) 
    def run(self):
        return Logger.LogMethod(self.service.run) 
    def detect(self, frame):
        return Logger.LogMethod(self.service.detect, frame) 
    def pick_best(self):
        return Logger.LogMethod(self.service.pick_best) 
    def scanning_for_plate(self,cut_frame):
        return Logger.LogMethod(self.service.scanning_for_plate,cut_frame) 
class Detector:
    def __init__(self):
        self.detected_lp = []
        self.actual_lp = ""
    def get_camera_cap(self) :
        cap = cv2.VideoCapture(1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, ConfigManager.DetectorConfig.cam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, ConfigManager.DetectorConfig.cam_height)
        return cap
    
    def run(self):
        cap = self.get_camera_cap()
        while True:
            ret, frame = cap.read()        
            if not ret:
                break
                    
            self.detect(frame)
            if len(self.actual_lp) > 0:
                print(self.actual_lp)
            cv2.imshow(f"CAM{str(ConfigManager.DetectorConfig.cam_number)}", frame)
            if cv2.waitKey(60) == 27:
                break

    def detect(self, frame) -> None:
        res, detections = scanner.scan_for_car(frame)
        if res:
            for detect in detections:
                x1,y1,x2,y2, _, = detect
                cut_frame = frame[int(y1) : int(y2), int(x1) : int(x2), :]
                self.scanning_for_plate(cut_frame)
            
    def pick_best(self):
        if len(self.detected_lp) > 10:
            best = scanner.pick_best_lp(self.detected_lp)
            self.detected_lp = []
            self.actual_lp = best
            
            
    def scanning_for_plate(self, cut_frame):
        suc, plate = scanner.scan_for_plate(cut_frame)
        if suc == -1:
            px1, py1, px2, py2, _, _ = plate
            code, scan = scanner.extract_plate(cut_frame,px1,py1,px2,py2)
            if code == -1:
                self.detected_lp.append(scan)
        self.pick_best()
                    
                    
            
       