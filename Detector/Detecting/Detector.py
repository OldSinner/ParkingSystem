from Detecting.Reader import Reader
from Helpers.cv2short import *
from Detecting.DetectorEnums import *
from Helpers.const import *
from datetime import datetime
from Communication.Broker import *
from Configuration.Configuration import *
import cv2
import os
import threading
import matplotlib.pyplot as plt


class Detector:
    def __init__(self):
        # Config
        config = Configuration()
        self.config: DetectorConfiguration = config.DetectorConfig
        self.state: DetectorState = DetectorState.SCANNING_FOR_CAR
        self.stats: DetectorStats = DetectorStats()
        # ---------------------  Reading  --------------------
        self.reader: Reader = Reader(config)
        self.frame_without_car = 0
        # ---------------------  Communication  --------------------
        self.BrokerSender: BrokerSender = BrokerSender(self)
        self.BrokerReceiver: BrokerReceiver = BrokerReceiver(self)
        self.RunBrokers()
        # ---------------------  Camera  --------------------
        if not self.config.use_photo:
            cap = self.get_video_capture()
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.cam_width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.cam_height)
            self.cap = cap

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.BrokerReceiver.Dispose()

    def RunBrokers(self):
        threading.Thread(target=self.BrokerReceiver.Consume, daemon=True).start()

    def Run(self):
        # Main Loop
        ret = True
        while ret:
            ret, frame = self.get_frame()
            match self.state:
                case DetectorState.SCANNING_FOR_CAR:
                    self.ScanCar(frame)
                case DetectorState.PROCESSING_CAR:
                    self.ScanLP(frame)
                case DetectorState.WAITING_FOR_GATE_CLOSE:
                    pass
                case DetectorState.WAITING_FOR_GATE_OPEN:
                    pass
            self.stats.DetectorState = self.state

            self.DrawDetectionRegions(frame)
            # cv2.imshow(f"CAM{str(self.config.cam_number)}", frame)
            plt.imshow(frame)
            self.reader.Clean()
            print(self.stats)
            key = cv2.waitKey(60)
            if key == 27:
                break

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
        if detected:
            self.frame_without_car = 0
            res, text = self.reader.FindPlate(frame, detections)
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
        self.SaveFiles(frame, text, self.reader.actual_lp, self.reader.actual_car)

    def ScanCar(self, frame):
        detected, detections = self.reader.ScanForCar(frame)
        self.stats.CarCount = len(detections)
        if detected:
            self.state = DetectorState.PROCESSING_CAR
            return (detected, detections)
        else:
            return (False, [])

    def SaveFiles(self, frame, lp_number, lp, car) -> None:

        current_date = datetime.now().strftime("%m%d%YT%H%M%S")
        folder_name = f"{lp_number}_{current_date}"
        path = os.path.join(PATH_TO_FILE, folder_name)
        os.makedirs(path, exist_ok=True)

        filepath_c = os.path.join(path, f"Car_{lp_number}.jpg")
        filepath_lp = os.path.join(path, f"LP_{lp_number}.jpg")
        # TODO: Fix Car photo saving
        cx1, cy1, cx2, cy2, _ = car
        x1, y1, x2, y2, score, _ = lp

        lp_crop = frame[int(y1) : int(y2), int(x1) : int(x2), :]
        car_Crop = frame[int(cy1) : int(cy2), int(cx1) : int(cx2), :]
        cv2.imwrite(filepath_c, car_Crop)
        cv2.imwrite(filepath_lp, lp_crop)

        self.BrokerSender.SendOpenGateSignal()


class DetectorStats:

    def __init__(self) -> None:
        self.CarCount = 0
        self.DetectorState = DetectorState.SCANNING_FOR_CAR
        self.ActualLp = ""
        self.GateStatus = GateState.CLOSED

    def __repr__(self) -> str:
        return (
            f"DetectorStats(CarCount={self.CarCount}, "
            f"DetectorState={self.DetectorState}, "
            f"ActualLp='{self.ActualLp}', "
            f"GateStatus={self.GateStatus})"
        )
