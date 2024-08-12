from ultralytics import YOLO
from const import *
from Detector.Sort.sort import *
import cv2
class Detector:
    def __init__(self) -> None:
        self.car_model = YOLO(CAR_DETECTOR_MODEL)
        self.license_playe = YOLO(LICENCE_PLATE_MODEL)
        self.cap = cv2.VideoCapture(VIDEO_PATH)
        self.mot_tracker = Sort()
        pass
    def detect(self) -> None:
        ret = True
        frame_nr = -1

        while ret :
            # Some preparing
            frame_nr += 1
            ret, frame = self.prepare_frame()
            # Detection
            cars = self.detect_cars(frame)
            #  Display 
            key = self.display(frame)
            if key == 27:
                break
            if ret:
                pass

    def prepare_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.resize(frame,(1280,720))
        return ret,frame

    def display(self, frame):
        cv2.imshow("Frame",frame)
        key = cv2.waitKey(30)
        return key
    
    def detect_cars(self, frame) -> list:
        detections = self.car_model(frame)[0]
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in VEHICLES_IDS:
                detections_.append([x1, y1, x2, y2, score])
        return detections_
    
    def track(self,list) -> np.NDArray:
       return self.mot_tracker.update(np.asarray(list))
    
    def find_plates(self,frame) -> None:
        pass