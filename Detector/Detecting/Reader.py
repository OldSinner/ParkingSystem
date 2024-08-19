from ultralytics import YOLO
from Communication.Logger import LoggerClass
from Helpers.const import *
from Helpers.lp_format import *
from Helpers.cv2short import *
from Configuration.Configuration import *
import cv2
import easyocr
from collections import Counter


class Reader:
    def __init__(self, Configuration: Configuration, logger: LoggerClass) -> None:
        self.config: ReaderConfiguration = Configuration.ReaderConfig
        # Models
        self.car_model = YOLO(self.config.car_detector_model)
        self.license_plate = YOLO(self.config.license_plate_model)
        # Reader
        self.reader = easyocr.Reader(["en"], gpu=True)
        # Position
        self.actual_car = (-1, -1, -1, -1, -1)
        self.actual_lp = (-1, -1, -1, -1, -1, -1)
        # Lp to determinate beetwen frames
        self.detected_lp = []

    def ScanForCar(self, frame) -> tuple[bool, list]:
        detections = self.car_model(frame, verbose=False)[0]
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in self.config.vehicles_ids:
                detections_.append([x1, y1, x2, y2, score])
        if len(detections_) > 0:
            return (True, detections_)
        else:
            return (False, detections_)

    def Clean(self) -> None:
        self.Logger.LogInfo("Clean", "Resetting Reader")
        self.actual_car = (-1, -1, -1, -1, -1)
        self.actual_lp = (-1, -1, -1, -1, -1, -1)

    # -1 - Detected Correctly
    # 0 - Detected More than one
    # 1 - Not detected
    # 2 - Still processing
    def FindPlate(self, frame, cars) -> tuple[int, str]:
        plates = self.license_plate(frame, verbose=False)[0]
        if len(plates) > 1:
            return (0, "")
        elif len(plates) == 1:
            for plate in plates.boxes.data.tolist():
                x1, y1, x2, y2, _, _ = plate
                # process lp
                code, tx = self.ExtractPlate(frame, x1, y1, x2, y2)
                if code == -1:
                    self.detected_lp.append(tx)
                if len(self.detected_lp) > LP_READING_TRY:
                    return self.pick_best_lp(plate, cars)
                return (2, "")
        else:
            return (2, "")

    # TODO Rename this here and in `FindPlate`
    def pick_best_lp(self, plate, cars):
        self.Logger.LogInfo("FindPlate", f"Picking best lp from {LP_READING_TRY} tries")
        counter = Counter(self.detected_lp)
        self.PickCar(plate, cars)
        lp = counter.most_common(1)[0][0]
        self.detected_lp = []
        return (-1, lp)

    def ExtractPlate(self, frame, x1, y1, x2, y2):
        lp_crop = frame[int(y1) : int(y2), int(x1) : int(x2), :]
        lp_gray_cop = cv2.cvtColor(lp_crop, cv2.COLOR_BGR2GRAY)
        _, lp_gray_treshhold = cv2.threshold(
            lp_gray_cop, 127, 255, cv2.THRESH_BINARY_INV
        )
        lps = self.ExtractLP(lp_gray_treshhold)
        code, tx = format_license_plate(lps)
        return code, tx

    def PickCar(self, plate, detections):
        # self.tracked_car
        x1, y1, x2, y2, _, _ = plate
        foundIt = False
        for i in range(len(detections)):
            xcar1, ycar1, xcar2, ycar2, _ = detections[i]
            if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
                car_indx = i
                foundIt = True
                break
        if foundIt:
            self.actual_car = detections[car_indx]
            self.actual_lp = plate
        self.actual_car = (-1, -1, -1, -1, -1)

    def ExtractLP(self, frame):
        detections = self.reader.readtext(frame)
        detected_words = []
        for detection in detections:
            _, text, _ = detection
            detected_words.append(text)
        return detected_words
