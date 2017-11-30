import cv2
import os, sys
import time

dev = int(sys.argv[1])
print("Opening capture device")
cap = cv2.VideoCapture(dev)
folder = sys.argv[2]
os.system("v4l2-ctl -d %i -c focus_auto=0" % dev)

if not os.path.isdir(folder):
    os.mkdir(folder)

path = os.path.join(folder, "image%03d.png")
j = 0
fps = 15
max_focus = 255
step_size = 3
multiplier = float(max_focus) / fps
i = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name)) and "image" in name])

while True:
    j = (j+1) % fps
    if j % step_size == 0:
        os.system("v4l2-ctl -d %i -c focus_absolute=%i" % (dev, int(multiplier*j)))
    time.sleep(0.1)
    ret, frame = cap.read()
    if frame is None or len(frame) < 1:
        continue
    cv2.imshow("image", frame)
    c = chr(cv2.waitKey(10) & 0xFF)
    if c == "q":
        break
    cv2.imwrite(path % i, frame)
    i+=1

