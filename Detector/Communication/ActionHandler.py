from Communication.CommunicationModels import *
from Communication.ActionEnums import *
from Detecting.DetectorEnums import *

class ActionHandler:
    def __init__(self, detector) -> None:
        self.detector = detector

    def MakeActionOnRes(self, rs:ActionResponse):
        if rs.Success == True:
            if rs.ActionType == ActionTypes.GATE_HANDLING.value:
                if rs.Action == GateHandlingAction.OPENED.value:
                    self.detector.stats.GateStatus = GateState.OPEN

                if rs.Action == GateHandlingAction.CLOSED.value:
                    self.detector.stats.GateStatus = GateState.CLOSED
