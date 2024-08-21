from ..logger import LoggerClass
from ..config import Configuration, DetectorConfiguration
import cv2

class Detector:
    def __init__(self,logger : LoggerClass, config : Configuration):
        self.config : DetectorConfiguration = config.DetectorConfig
        self.logger = logger;
    def get_camera_cap(self):
        self.logger.LogInfo("Detector.get_camera_cap", 'Catching Video Capture "1"')
        try:
            cap = cv2.VideoCapture(1)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.cam_width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.cam_height)
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
                cv2.imshow(f"CAM{str(self.config.cam_number)}", frame)
                key = cv2.waitKey(120)
                if key == 27:
                    break
        except Exception as ex:
            self.logger.LogErr("Detector.Run", ex)