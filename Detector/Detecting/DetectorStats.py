from Detecting.DetectorEnums import DetectorState, GateState


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
