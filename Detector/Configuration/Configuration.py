import configparser
import ast
import os
class Configuration:
    def __init__(self) -> None:
        # Read Configurtaion
        config = configparser.ConfigParser()
        config.read('./ConfigurationFiles/DetectorConfig.ini')
        # Build Reader tab
        readerdict = {
            'car_detector_model' : config.get('Reader', 'car_detector_model'),
            'license_plate_model' : config.get('Reader', 'license_plate_model'),
            'vehicles_ids' : ast.literal_eval(config.get('Reader', 'vehicles_ids'))
            }
        

        # Build Object for Segments
        self.ReaderConfig = ReaderConfiguration(readerdict)



class ReaderConfiguration:
    def __init__(self, yolo) -> None:
        self.car_detector_model = yolo['car_detector_model']
        self.license_plate_model = yolo['license_plate_model']
        self.vehicles_ids = yolo['vehicles_ids']