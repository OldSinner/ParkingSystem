from enum import Enum

class ActionTypes(Enum):
    NONE = 0
    GATE_HANDLING = 1

class GateHandlingAction(Enum):
    NONE = 0
    OPENED = 1
    CLOSED = 2
