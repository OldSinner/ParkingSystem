import cv2
from const import *

def cv2short_rect_car(frame,x1,y1,x2,y2):
    cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),CAR_COLOR,CAR_THICK)
