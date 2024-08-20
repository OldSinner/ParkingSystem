from enum import Enum

class DetectorState(Enum):
    SCANNING_FOR_CAR = 1
    PROCESSING_CAR = 2
    WAITING_FOR_GATE_OPEN = 3
    WAITING_FOR_GATE_CLOSE = 4

class GateState(Enum):
    OPEN = 1,
    CLOSED = 2
