from ..config import ConfigManager
from ultralytics import YOLO
import easyocr
from collections import Counter
import cv2
from ..formatters import format_license_plate
scanner_config = ConfigManager.ReaderConfig
from ..logger import Logger as Logger
import time
class ScannerLog:
    def __init__(self) -> None:
        self.scanner = Scanner()
    def scan_for_car(self,frame) -> tuple[bool, list]:
        return Logger.LogDebugMethod(self.scanner.scan_for_car,frame) 
    def scan_for_plate(self,frame) -> tuple[int, list]:
        return Logger.LogMethod(self.scanner.scan_for_plate,frame) 
    def extract_plate(self,frame, x1, y1, x2, y2) -> tuple[int, str]:
        return Logger.LogMethod(self.scanner.extract_plate,frame, x1, y1, x2, y2) 
    def read_plate(self,frame) -> list:
        return Logger.LogMethod(self.scanner.read_plate,frame) 
    def pick_best_lp(self,detected_lp) -> str:
        return Logger.LogMethod(self.scanner.pick_best_lp,detected_lp) 
class Scanner:
    def __init__(self) -> None:
        self.config = ConfigManager.ReaderConfig
        self.car_model = YOLO(self.config.car_detector_model)
        self.license_plate = YOLO(self.config.license_plate_model)
        self.reader = easyocr.Reader(["en"], gpu=True)
    # 
   
    def scan_for_car(self,frame) -> tuple[bool, list]:
        detections = self.car_model(frame, verbose=False, device='0')[0]
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in self.config.vehicles_ids:
                detections_.append([x1, y1, x2, y2, score])
        return (True, detections_) if detections_ else (False, detections_)
    # 
    def scan_for_plate(self,frame) -> tuple[int,list]:
        plates = self.license_plate(frame, verbose=False, device='0')[0]
        if len(plates) > 1:
            return (0, [])
        elif len(plates) == 1:
            return (-1, plates.boxes.data.tolist()[0])
        else:
            return (2,[])
        
    def extract_plate(self, frame, x1, y1, x2, y2) -> tuple[int,str]:
        lp_crop = frame[int(y1) : int(y2), int(x1) : int(x2), :]
        
        lp_gray_cop = cv2.cvtColor(lp_crop, cv2.COLOR_BGR2GRAY)
        _, lp_gray_threshold = cv2.threshold(
            lp_gray_cop, 127, 255, cv2.THRESH_BINARY_INV
        )
        
        lps = self.read_plate(lp_gray_threshold)
        code, tx = format_license_plate(lps)
        return code, tx
    def read_plate(self,frame) -> list:
        detections = self.reader.readtext(frame)
        detected_words = []
        for detection in detections:
            _, text, _ = detection
            detected_words.append(text)
        return detected_words
    
    def pick_best_lp(self,detected_lp) -> str:
        counter = Counter(detected_lp)
        return counter.most_common(1)[0][0]
    
    