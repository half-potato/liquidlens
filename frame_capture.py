import cv2
import os, sys

cap = cv2.VideoCapture(int(sys.argv[1]))
folder = sys.argv[2]

if not os.path.isdir(folder):
    os.mkdir(folder)

path = os.path.join(folder, "image%03d.png")

i = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name)) and "image" in name])
while True:
    ret, frame = cap.read()
    if frame is None or len(frame) < 1:
        continue
    cv2.imshow("image", frame)
    c = chr(cv2.waitKey(10) & 0xFF)
    if c == "q":
        break
    if c == "s":
        cv2.imwrite(path % i, frame)
        i+=1
