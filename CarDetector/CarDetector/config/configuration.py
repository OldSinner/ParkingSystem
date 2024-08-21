import configparser
import ast


class Configuration:
    def __init__(self) -> None:
        # Read Configuration
        config = configparser.ConfigParser()
        config.read("./CarDetector/config/DetectorConfig.ini")
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
            #
            "path_to_file": config.get("Detector", "path_to_file"),
            "save_to_file": ast.literal_eval(config.get("Detector", "save_to_file")),
        }
        #
        # Build CV2 tab
        cv2_dict = {
            "stat_color": ast.literal_eval(config.get("CV2", "stat_color")),
            "picked_car": ast.literal_eval(config.get("CV2", "picked_car")),
            "picked_lp": ast.literal_eval(config.get("CV2", "picked_lp")),
            "car_color": ast.literal_eval(config.get("CV2", "car_color")),
            "car_thick": config.getint("CV2", "car_thick"),
            "stat_thick": config.getint("CV2", "stat_thick"),
        }

        # Build MQ Configuration:
        mq_dict = {
            "url": config.get("MQ", "url"),
            "gate_action_queue": config.get("MQ", "gate_action_queue"),
            "gate_event_queue": config.get("MQ", "gate_event_queue"),
            "logger_exchange": config.get("MQ", "logger_exchange"),
        }

        # Build Object for Segments
        self.ReaderConfig = ReaderConfiguration(reader_dict)
        self.DetectorConfig = DetectorConfiguration(detector_dict)
        self.CV2Configuration = CV2Configuration(cv2_dict)
        self.MQConfiguration = MQConfiguration(mq_dict)


class DetectorConfiguration:
    def __init__(self, detector_dict) -> None:
        self.cam_number : int = detector_dict["cam_number"]
        self.cam_width : int= detector_dict["cam_width"]
        self.cam_height : int= detector_dict["cam_height"]
        #
        self.path_to_file :str = detector_dict["path_to_file"]
        self.save_to_file :bool = detector_dict["save_to_file"]


class ReaderConfiguration:
    def __init__(self, yolo) -> None:
        self.car_detector_model :str = yolo["car_detector_model"]
        self.license_plate_model :str = yolo["license_plate_model"]
        self.vehicles_ids :list[str]= yolo["vehicles_ids"]


class CV2Configuration:
    def __init__(self, cv2_dict: dict[str, any]) -> None: # type: ignore
        self.stat_color :tuple[int,int,int] = cv2_dict.get("stat_color", (0,0,0))
        self.picked_car :tuple[int,int,int] = cv2_dict.get("picked_car", (0,0,0))
        self.picked_lp :tuple[int,int,int] = cv2_dict.get("picked_lp", (0,0,0))
        self.car_color :tuple[int,int,int] = cv2_dict.get("car_color", (0,0,0))
        self.car_thick :int= cv2_dict.get("car_thick", "")
        self.stat_thick :int= cv2_dict.get("stat_thick", "")


class MQConfiguration:
    def __init__(self, mq_dict: dict[str, any]) -> None:  # type: ignore
        self.url : str = mq_dict.get("url", "") 
        self.gate_action_queue : str = mq_dict.get("gate_action_queue", "")
        self.gate_event_queue : str = mq_dict.get("gate_event_queue", "")
        self.logger_exchange : str = mq_dict.get("logger_exchange", "")
