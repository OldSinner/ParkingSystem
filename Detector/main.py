from detector import *
import cv2

# detector = Detector()
# detector.detect_from_img()

cap = cv2.VideoCapture(1)
frame_rate = 10
prev = 0
while True:
    time_elapsed = time.time() - prev
    _, frame = cap.read()
    if time_elapsed > 1./frame_rate:
        prev = time.time()
        cv2.imshow("OBS",frame)

        # Do something with your image here.
   