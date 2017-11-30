import cv2, os, sys, time, util

dev = int(sys.argv[1])
print("Opening capture device")
cap = cv2.VideoCapture(dev)
folder = sys.argv[2]
os.system("v4l2-ctl -d %i -c focus_auto=0" % dev)

if not os.path.isdir(folder):
    os.mkdir(folder)

path = os.path.join(folder, "image%03d.png")
i = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name)) and "image" in name])

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

focuses = xrange(0, 255, 25)

for f in focuses:
    os.system("v4l2-ctl -d %i -c focus_absolute=%i" % (dev, f))
    print(util.focus_to_focal_length(f))
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

