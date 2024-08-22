from ..core.scanner import ScannerLog
from ..logger import LoggerClass
import cv2
from ..config import ConfigManager
class Detector:
    def __init__(self,logger : LoggerClass):
        self.logger = logger;
        self.scanner = ScannerLog(logger)
        
    def get_camera_cap(self):
        self.logger.LogInfo("Detector.get_camera_cap", 'Catching Video Capture "1"')
        try:
            cap = cv2.VideoCapture(1)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, ConfigManager.DetectorConfig.cam_width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, ConfigManager.DetectorConfig.cam_height)
        except Exception as ex:
            self.logger.LogErr("Detector.get_camera_cap", ex)
        return cap
    
    def run(self):
        self.logger.LogInfo("Detector.Run", "Starting detector...")
        cap = self.get_camera_cap()
        try:
            while True:
                ret, frame = cap.read()        
                if not ret:
                    break
                
                self.detect()
                
                cv2.imshow(f"CAM{str(ConfigManager.DetectorConfig.cam_number)}", frame)
                if cv2.waitKey(120) == 27:
                    break
        except Exception as ex:
            self.logger.LogErr("Detector.Run", ex)

    def detect(self) -> None:
        pass
       