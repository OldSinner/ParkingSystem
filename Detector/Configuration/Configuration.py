import configparser
import ast
import os


class Configuration:
    def __init__(self) -> None:
        # Read Configurtaion
        config = configparser.ConfigParser()
        config.read("./ConfigurationFiles/DetectorConfig.ini")
        # Build Reader tab
        reader_dict = {
            "car_detector_model": config.get("Reader", "car_detector_model"),
            "license_plate_model": config.get("Reader", "license_plate_model"),
            "vehicles_ids": ast.literal_eval(config.get("Reader", "vehicles_ids")),
        }

        # Build Detector tab
        detector_dict = {
            "cam_number": config.getint("Detector", "cam_number"),
            "cam_width": config.getint("Detector", "cam_width"),
            "cam_height": config.getint("Detector", "cam_height"),
        }

        # Build Object for Segments
        self.ReaderConfig = ReaderConfiguration(reader_dict)
        self.DetectorConfig = DetectorConfiguration(detector_dict)


class DetectorConfiguration:
    def __init__(self, detector_dict) -> None:
        self.cam_number = detector_dict["cam_number"]
        self.cam_width = detector_dict["cam_width"]
        self.cam_height = detector_dict["cam_height"]


class ReaderConfiguration:
    def __init__(self, yolo) -> None:
        self.car_detector_model = yolo["car_detector_model"]
        self.license_plate_model = yolo["license_plate_model"]
        self.vehicles_ids = yolo["vehicles_ids"]
