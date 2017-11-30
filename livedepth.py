import cv2
from scipy import ndimage
import os, sys
import numpy as np
import depthtofocus
import time

if len(sys.argv) != 2:
    print("Use: python livedepth.py CAMERA_DEV_NUM")
    exit()
dev = int(sys.argv[1])
print("Opening capture device")
cap_s = "nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)I420, framerate=(fraction)24/1 ! nvvidconv flip-method=2 ! videoconvert ! appsink"
cap = cv2.VideoCapture(dev)
cap.set(3, 640)
cap.set(4, 480)

print("Disabling auto focus")
os.system("v4l2-ctl -d %i -c focus_auto=0" % dev)

print("Waiting for camera")
null_frame_count = 0
while True:
    ret, frame = cap.read()
    if null_frame_count > 30:
        print("Unable to open device")
        exit()
    if frame is None or len(frame) < 1:
        print("No image")
        null_frame_count += 1
        continue
    if not (frame is None or len(frame) < 1):
        break

measure_per_depth = 8
max_focus = 255
step_size = 255.0/measure_per_depth
focus_measures = []
focuses = np.array(range(measure_per_depth)) * step_size

print("Starting loop")
while True:
    for i in focuses:
        os.system("v4l2-ctl -d %i -c focus_absolute=%i" % (dev, int(i)))
        time.sleep(0.1)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        focus = depthtofocus.gray_to_focus(frame)
        cv2.imshow("frame", focus)
        focus_measures.append(focus)
        if chr(cv2.waitKey(10) & 0xFF) == "q":
            break
    print("Calc depth")
    depth = depthtofocus.calc_depth(np.array(focuses) / 20, np.array(focus_measures), 1)
    s = depthtofocus.scale(depth)
    col = cv2.applyColorMap(s, cv2.COLORMAP_JET)
    cv2.imshow("depth", depth)
    focus_measures = []
    if chr(cv2.waitKey(10) & 0xFF) == "q":
        break

cap.release()

