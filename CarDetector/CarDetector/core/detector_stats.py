class DetectorStats:
    def __init__(self) -> None:
        self.CarCount = 0
        self.ActualLp = ""

    def __repr__(self) -> str:
        return (
            f"DetectorStats(CarCount={self.CarCount}, "
            f"ActualLp='{self.ActualLp}', "
        )
