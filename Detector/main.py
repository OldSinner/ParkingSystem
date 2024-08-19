from Detecting.Detector import Detector
from Communication.Logger import LoggerClass
from Configuration.Configuration import Configuration

config = Configuration()
logger = LoggerClass(config.MQConfiguration)
with Detector(logger, config) as detector:
    detector.Run()
