import cv2
from scipy import ndimage
import os, sys
import numpy as np

dev = int(sys.argv[1])
print("Opening capture device")
cap = cv2.VideoCapture(dev)
cap.set(3, 640)
cap.set(4, 480)

print("Disabling auto focus")
os.system("v4l2-ctl -d %i -c focus_auto=0" % dev)
i = 0
fps = 15
max_focus = 255
step_size = 3
multiplier = float(max_focus) / fps

null_frame_count = 0
focus_measures = []
focuses = []

print("Starting loop")
while True:
    i = (i+1) % fps
    if i % step_size == 0:
        os.system("v4l2-ctl -d %i -c focus_absolute=%i" % (dev, int(multiplier*i)))
    ret, frame = cap.read()
    if null_frame_count > 30:
        print("Unable to open device")
        break
    if frame is None or len(frame) < 1:
        print("No image")
        null_frame_count += 1
        continue
    print(frame.shape)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("frame", gray)
    if chr(cv2.waitKey(10) & 0xFF) == "q":
        break
