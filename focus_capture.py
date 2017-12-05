import cv2, os, sys, time, util

dev = int(sys.argv[1])
folder = sys.argv[2]

# Directory stuff
if not os.path.isdir(folder):
    os.mkdir(folder)

path = os.path.join(folder, "image%03d.png")
i = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name)) and "image" in name])

# Capture
cap = util.openCamera(dev)
os.system("v4l2-ctl -d %i -c focus_auto=0" % dev)

focuses = xrange(10, 255, 5)
focal_lengths = [util.focus_to_focal_length(i) for i in xrange(0, 255, 25)]
csv = "".join(["%f,\n" % i for i in focal_lengths])
with open("focuses.csv", "w+") as f:
    f.write(csv)

for f in focuses:
    os.system("v4l2-ctl -d %i -c focus_absolute=%i" % (dev, f))
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

