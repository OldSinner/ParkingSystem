import cv2
from Configuration.Configuration import *
from Helpers.const import *
from datetime import datetime

MARGIN = 20
TEXT_SPACE = 30
ConfigurationManager = Configuration()
config: CV2Configuration = ConfigurationManager.CV2Configuration


def cv2short_rect_car(frame, x1, y1, x2, y2):
    cv2.rectangle(
        frame,
        (int(x1), int(y1)),
        (int(x2), int(y2)),
        config.car_color,
        config.car_thick,
    )


def cv2short_rect_pick_car(frame, x1, y1, x2, y2):
    cv2.rectangle(
        frame,
        (int(x1), int(y1)),
        (int(x2), int(y2)),
        config.picked_car,
        config.car_thick,
    )


def cv2short_rect_lp(frame, x1, y1, x2, y2):
    cv2.rectangle(
        frame,
        (int(x1), int(y1)),
        (int(x2), int(y2)),
        config.picked_lp,
        config.car_thick,
    )


def cv2draw_stats(frame, stats):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    cv2.putText(
        frame,
        f"Time: {current_time}",
        (MARGIN, MARGIN + 0 * TEXT_SPACE),
        1,
        1.5,
        config.stat_color,
        config.stat_thick,
    )
    cv2.putText(
        frame,
        f"Car detected: {str(stats.CarCount)}",
        (MARGIN, MARGIN + 1 * TEXT_SPACE),
        1,
        1.5,
        config.stat_color,
        config.stat_thick,
    )
    cv2.putText(
        frame,
        f"Detector state: {str(stats.DetectorState)}",
        (MARGIN, MARGIN + 2 * TEXT_SPACE),
        1,
        1.5,
        config.stat_color,
        config.stat_thick,
    )
    cv2.putText(
        frame,
        f"Detected LP: {str(stats.ActualLp)}",
        (MARGIN, MARGIN + 3 * TEXT_SPACE),
        1,
        1.5,
        config.stat_color,
        config.stat_thick,
    )
    cv2.putText(
        frame,
        f"Gate Status: {str(stats.GateStatus)}",
        (MARGIN, MARGIN + 4 * TEXT_SPACE),
        1,
        1.5,
        config.stat_color,
        config.stat_thick,
    )

    # cv2.putText(frame,"DETECTED CARS: "+ )
