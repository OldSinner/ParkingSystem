CAR_DETECTOR_MODEL = "./Detector/Models/yolov8n.pt"
LICENCE_PLATE_MODEL = "./Detector/Models/license_plate_detector.pt" # https://github.com/Muhammad-Zeerak-Khan/Automatic-License-Plate-Recognition-using-YOLOv8
VIDEO_PATH = "./TestData/testvideo.mp4"
VEHICLES_IDS = [2,3,5,7]
CAM_NUMBER = 1

STAT_COLOR = (255,0,0)

PICKED_CAR = (0,255,255)
PICKED_LP = (0,0,255)
CAR_COLOR = (0,255,0)
CAR_THICK = 2
STAT_THICK = 2

FRAME_WITHOUT_CAR = 10
LP_READING_TRY = 10

PATH_TO_FILE = "C:/ParkingSystem/"

CAM_WIDTH = 1280
CAM_HEIGHT = 720

APP_NAME = "DETECTOR_GATE_IN_1"
MQ_URL = "localhost"

GATE_HANDLER = "GATE_HANDLER"

# https://github.com/abewley/sort/blob/master/sort.py object tracking