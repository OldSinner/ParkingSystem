from ..core.scanner import ScannerLog
import cv2
from ..config import ConfigManager
from ..logger import Logger
class DetectorLog:
    def __init__(self):
        self.service = Detector()
    def get_camera_cap(self):
        return Logger.LogMethod(self.service.get_camera_cap) 
    def run(self):
        return Logger.LogMethod(self.service.run) 
    def detect(self, frame):
        return Logger.LogMethod(self.service.detect, frame) 
class Detector:
    def __init__(self):
        pass        
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
                    
            cv2.imshow(f"CAM{str(ConfigManager.DetectorConfig.cam_number)}", frame)
            if cv2.waitKey(120) == 27:
                break

    def detect(self, frame) -> None:
        pass
       