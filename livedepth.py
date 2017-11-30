import cv2
from scipy import ndimage
import os, sys, depthtofocus, time, util
import numpy as np

if len(sys.argv) != 2:
    print("Use: python livedepth.py CAMERA_DEV_NUM")
    exit()
dev = int(sys.argv[1])
print("Opening capture device")
cap_s = "nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)I420, framerate=(fraction)24/1 ! nvvidconv flip-method=2 ! videoconvert ! appsink"
cap = util.openCamera(dev)

print("Disabling auto focus")
os.system("v4l2-ctl -d %i -c focus_auto=0" % dev)

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

