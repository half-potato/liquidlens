import cv2
from scipy import ndimage
import os, sys
import numpy as np
import depthtofocus

dev = int(sys.argv[1])
print("Opening capture device")
cap_s = "nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)I420, framerate=(fraction)24/1 ! nvvidconv flip-method=2 ! videoconvert ! appsink"
cap = cv2.VideoCapture(dev)
cap.set(3, 640)
cap.set(4, 480)

print("Disabling auto focus")
#os.system("v4l2-ctl -d %i -c focus_auto=0" % dev)
i = 0
fps = 30
max_focus = 255
step_size = 3
multiplier = float(max_focus) / fps
null_frame_count = 0
focus_measures = []
focuses = []

print("Starting loop")
while True:
    #i = (i+max_focus/float(fps)) % (max_focus+1)
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
    print(len(focus_measures))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("frame", gray)
    lap = cv2.GaussianBlur(modified_laplace(gray), (9,9), 0)
    mean = ndimage.convolve(lap, mean_kernel, mode="constant")
    if i % step_size == 5:
        focus_measures.append(lap)
        focuses.append(multiplier * float(i+1))
    if len(focus_measures) >= 14:
        print("Calc depth")
        depth = calc_depth(np.array(focuses) / 20, np.array(focus_measures), 1)
        print(depth)
        s = scale(depth)
        col = cv2.applyColorMap(s, cv2.COLORMAP_JET)
        focus_measures = []
        focuses = []
    if chr(cv2.waitKey(10) & 0xFF) == "q":
        break

cap.release()

