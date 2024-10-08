from datetime import datetime
import os
import threading
import cv2

from Communication.BrokerSender import BrokerSender
from Communication.Logger import LoggerClass
from Communication.Broker import *
from Detecting.DetectorStats import DetectorStats
from Detecting.Reader import Reader
from Detecting.DetectorEnums import *
from Helpers.cv2short import *
from Helpers.const import *
from Configuration.Configuration import *


class Detector:
    def __init__(self, Logger, config: Configuration):
        # Config
        self.config: DetectorConfiguration = config.DetectorConfig
        self.state: DetectorState = DetectorState.SCANNING_FOR_CAR
        self.stats: DetectorStats = DetectorStats()

        # Reading
        self.reader: Reader = Reader(config, Logger)
        self.frame_without_car = 0

        # Communication
        self.Logger: LoggerClass = Logger
        self.BrokerSender: BrokerSender = BrokerSender(
            self, config.MQConfiguration, Logger
        )
        self.BrokerReceiver: BrokerReceiver = BrokerReceiver(
            self, config.MQConfiguration, Logger
        )
        self.RunBrokers()

        # Camera
        if not self.config.use_photo:
            self.get_camera_cap()
        else:
            self.Logger.LogInfo(
                "Detector.get_camera_cap",
                f"Using a image from {self.config.cam_photo_path}",
            )

    def get_camera_cap(self):
        self.Logger.LogInfo("Detector.get_camera_cap", 'Catching Video Capture "1"')
        try:
            cap = cv2.VideoCapture(1)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.cam_width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.cam_height)
            self.cap = cap
        except Exception as ex:
            self.Logger.LogErr("Detector.get_camera_cap", ex)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.BrokerReceiver.Dispose()

    def RunBrokers(self):
        self.Logger.LogInfo("Detector.RunBrokers", "Starting BrokerReceiver")
        threading.Thread(target=self.BrokerReceiver.Consume, daemon=True).start()

    def Run(self):
        self.Logger.LogInfo("Detector.Run", "Detector ON")
        try:
            while True:
                ret, frame = self.get_frame()
                if not ret:
                    break
                if self.state == DetectorState.SCANNING_FOR_CAR:
                    self.ScanCar(frame)
                elif self.state == DetectorState.PROCESSING_CAR:
                    self.ScanLP(frame)

                self.stats.DetectorState = self.state
                self.DrawDetectionRegions(frame)
                cv2.imshow(f"CAM{str(self.config.cam_number)}", frame)
                self.reader.Clean()
                key = cv2.waitKey(120)
                if key == 27:
                    break
        except Exception as ex:
            self.Logger.LogErr("Detector.Run", ex)

    def get_frame(self):
        if self.config.use_photo:
            return (True, cv2.imread(self.config.cam_photo_path))
        else:
            return self.cap.read()

    def DrawDetectionRegions(self, frame):

        cv2draw_stats(frame, self.stats)
        cx1, cy1, cx2, cy2, _ = self.reader.actual_car
        lx1, ly1, lx2, ly2, _, _ = self.reader.actual_lp
        cv2short_rect_pick_car(frame, cx1, cy1, cx2, cy2)
        cv2short_rect_lp(frame, lx1, ly1, lx2, ly2)

    def ScanLP(self, frame):
        detected, detections = self.ScanCar(frame)
        if not detected:
            self.frame_without_car = 0
            res, text = self.reader.FindPlate(frame, detections)
            if res == -1:
                self.Logger.LogInfo("Detector.ScanLP", f'Founded LP: "{text}"')
                self.ProcessCarAndLP(frame, text)
            return
        else:
            self.frame_without_car += 1
            if self.frame_without_car > FRAME_WITHOUT_CAR:
                self.Logger.LogWarn(
                    "Detector.ScanLP",
                    f"Lost car in sight for longer than {FRAME_WITHOUT_CAR} frames",
                )
                self.reader.detected_lp = []
                self.state = DetectorState.SCANNING_FOR_CAR

    def ProcessCarAndLP(self, frame, text):
        if self.stats.GateStatus == GateState.OPEN:
            self.state = DetectorState.WAITING_FOR_GATE_CLOSE
        else:
            self.state = DetectorState.WAITING_FOR_GATE_OPEN
        self.stats.ActualLp = text
        self.handle_save(frame, text, self.reader.actual_lp, self.reader.actual_car)

        self.Logger.LogInfo("Detector.ProcessCarAndLP", "Sending open signal")
        self.BrokerSender.SendOpenGateSignal()

    def ScanCar(self, frame):
        detected, detections = self.reader.ScanForCar(frame)
        self.stats.CarCount = len(detections)
        if detected:
            self.Logger.LogInfo(
                "Detector.ScanCar",
                f"Detected {len(detections)} cars, starting to process..",
            )
            self.state = DetectorState.PROCESSING_CAR
            return (detected, detections)
        else:
            return (False, [])

    def handle_save(self, frame, lp_number, lp, car) -> None:

        if not self.config.save_to_file:
            return
        try:
            self.save_files(lp_number, car, lp, frame)
        except Exception as ex:
            self.Logger.LogErr("Detector.SaveFiles", ex)

    def save_files(self, lp_number, car, lp, frame):
        current_date = datetime.now().strftime("%m%d%YT%H%M%S")
        folder_name = f"{lp_number}_{current_date}"
        path = os.path.join(self.config.path_to_file, folder_name)
        os.makedirs(path, exist_ok=True)
        self.Logger.LogInfo("Detector.SaveFiles", f"Prepared dir for photos {path}")
        #
        filepath_c = os.path.join(path, f"Car_{lp_number}.jpg")
        filepath_lp = os.path.join(path, f"LP_{lp_number}.jpg")
        # TODO: Fix Car photo saving
        cx1, cy1, cx2, cy2, _ = car
        x1, y1, x2, y2, score, _ = lp
        #
        lp_crop = frame[int(y1) : int(y2), int(x1) : int(x2), :]
        car_Crop = frame[int(cy1) : int(cy2), int(cx1) : int(cx2), :]
        self.Logger.LogInfo("Detector.SaveFiles", f"Saving car photos in {filepath_c}")
        cv2.imwrite(filepath_c, car_Crop)
        self.Logger.LogInfo("Detector.SaveFiles", f"Saving lp photos in {filepath_c}")
        cv2.imwrite(filepath_lp, lp_crop)
