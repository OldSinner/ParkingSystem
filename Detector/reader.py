from ultralytics import YOLO
from const import *
from Sort.sort import *
from cv2short import *
import cv2
import easyocr
class Reader:
    def __init__(self) -> None:
        self.car_model = YOLO(CAR_DETECTOR_MODEL)
        self.license_plate = YOLO(LICENCE_PLATE_MODEL)
        self.mot_tracker = Sort()
        self.frame_nr = -1
        self.reader = easyocr.Reader(['en'], gpu=True)
        pass

    def scan_for_car(self, frame) -> tuple[bool,list]:
        detection_list = self.detect_cars(frame)
        if len(detection_list) > 0:
            for detect in detection_list:
                x1, y1, x2, y2, score = detect
                cv2short_rect_car(frame,x1,y1,x2,y2)
            return (True,detection_list)
        else:
            return (False,[])
    
    def detect_cars(self, frame) -> list:
        detections = self.car_model(frame)[0]
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in VEHICLES_IDS:
                detections_.append([x1, y1, x2, y2, score])
        return detections_
    
    # def detect_from_img(self) -> None:
    #     self.frame_nr += 1
    #     ret, frame = self.prepare_frame_img()
    #     cars = self.detect_cars(frame)
    #     self.tracked_car = self.track(cars)
    #     self.find_plates(frame)
    #     key = self.display(frame)

    # def detect(self) -> None:
    #     ret = True

    #     while ret and self.frame_nr < 10:
    #         # Some preparing
    #         self.frame_nr += 1
    #         ret, frame = self.prepare_frame()
    #         # Detection
    #         cars = self.detect_cars(frame)
    #         self.tracked_car = self.track(cars)
    #         self.find_plates(frame)
    #         #  Display 
    #         key = self.display(frame)
    #         if key == 27:
    #             break
    #         if ret:
    #             pass
    # def prepare_frame_img(self):
    #     frame = cv2.imread("./TestData/test3.jpg")
    #     return True,frame
    # def prepare_frame(self):
    #     ret, frame = self.cap.read()
    #     frame = cv2.resize(frame,(1920,1080))
    #     return ret,frame

    # def display(self, frame):
    #     cv2.imshow("Frame",frame)
    #     key = cv2.waitKey(0)
    #     return key
    

    
    # def track(self,list) -> np.ndarray:
    #    return self.mot_tracker.update(np.asarray(list))
    
    # def find_plates(self,frame) -> None:
    #     plates = self.license_plate(frame)[0]
    #     for plate in plates.boxes.data.tolist():
    #         x1, y1, x2, y2, score, _ = plate
    #         cx1, cy1, cx2, cy2, cid = self.define_car(plate)
    #         # process lp
    #         lp_crop = frame[int(y1):int(y2),int(x1):int(x2),:]
    #         lp_gray_cop = cv2.cvtColor(lp_crop, cv2.COLOR_BGR2GRAY)
    #         _ , lp_gray_treshhold = cv2.threshold(lp_gray_cop,64,255,cv2.THRESH_BINARY_INV)

    #         lp, lps = self.read_lp(lp_gray_treshhold)
    
    # def define_car(self, plate) -> None:
    #     # self.tracked_car
    #     x1, y1, x2, y2, score, class_id = plate

    #     foundIt = False
    #     for i in range(len(self.tracked_car)):
    #         xcar1, ycar1, xcar2, ycar2, _ = self.tracked_car[i]
    #         if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
    #             car_indx = i
    #             foundIt = True
    #             break

    #     if foundIt:
    #         return self.tracked_car[car_indx]
    #     return -1,-1,-1,-1,-1
    
    # def read_lp(self, frame):
    #     detections = self.reader.readtext(frame)
    #     detected_words = []
    #     cv2.imshow("lp",frame)
    #     for detection in detections:
    #         bbox, text, score = detection
    #         detected_words.append(text)
    #     return detected_words
    
    