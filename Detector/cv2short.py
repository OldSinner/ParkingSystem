import cv2
from const import *
from datetime import datetime
MARGIN = 20
TEXT_SPACE = 30
def cv2short_rect_car(frame,x1,y1,x2,y2):
    cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),CAR_COLOR,CAR_THICK)
def cv2draw_stats(frame,stats):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    cv2.putText(frame,"Time: "+str(current_time),(MARGIN,MARGIN + 0*TEXT_SPACE),1,1.5,STAT_COLOR,STAT_THICK)
    # cv2.putText(frame,"DETECTED CARS: "+ )
