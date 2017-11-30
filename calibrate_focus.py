import cv2
from scipy import ndimage
import os, sys
import numpy as np

dev = int(sys.argv[1])
cap = cv2.VideoCapture(dev)
print(cap.isOpened())

os.system("v4l2-ctl -d %i -c focus_auto=0" % dev)
i = 0
max_focus = 255
step_size = 1
fine_tuning_iterations = 5
fine_tuning_batch_size = 10

# [x, y, h, w]
rect = [None, None, None, None]
is_drawing=False

def setCaptureRect(event, x, y, flags, param):
    global rect, is_drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        is_drawing=True
        rect = [x, y, None, None]
    elif event == cv2.EVENT_MOUSEMOVE:
        if is_drawing:
            ox = min(x, rect[0])
            oy = min(y, rect[1])
            tx = max(x, rect[0])
            ty = max(y, rect[1])
            w = tx - ox
            h = ty - oy
            #w = 40
            #h = 40
            #ox = 640/2 - w/2
            #oy = 480/2 - h/2
            rect = [ox, oy, w, h]
    elif event == cv2.EVENT_LBUTTONUP:
        is_drawing=False
        ox = min(x, rect[0])
        oy = min(y, rect[1])
        tx = max(x, rect[0])
        ty = max(y, rect[1])
        w = tx - ox
        h = ty - oy
        #w = 40
        #h = 40
        #ox = 640/2 - w/2
        #oy = 480/2 - h/2
        print(w, h)
        rect = [ox, oy, w, h]

x_kernel = np.array([[0, -1, 0], [0, 2, 0], [0, -1, 0]])
y_kernel = np.array([[0, 0, 0], [-1, 2, -1], [0, 0, 0]])
def modified_laplace(image):
    global x_kernel, y_kernel
    #dx = cv2.filter2D(image.astype(np.float32), -1, x_kernel)
    #dy = cv2.filter2D(image.astype(np.float32), -1, y_kernel)
    dx = ndimage.convolve(image, x_kernel, mode="constant")
    dy = ndimage.convolve(image, y_kernel, mode="constant")
    #return dx + dy
    return np.abs(dx) + np.abs(dy)

cv2.namedWindow("Laplacian")
cv2.setMouseCallback("Laplacian", setCaptureRect)

measurements = []
is_sweeping = False
is_fine_tuning = False

ft_wb_i = 0
ft_measurements = []

focus = 0

while True:
    if is_sweeping:
        i = (i+1) % max_focus
        if i == 0:
            is_sweeping = False
            is_fine_tuning = True
            ft_measurements = []
            ft_wb_i = 0
            measurements = np.array(measurements)
            measurements = measurements[(-1*measurements[:,0]).argsort()]
    if is_fine_tuning:
        ft_wb_i = ft_wb_i+1
        if ft_wb_i >= fine_tuning_batch_size*fine_tuning_iterations:
            is_fine_tuning=False
            # Sort ft_measurements and print top ten results
            ft_measurements = np.array(ft_measurements)
            ft_measurements = ft_measurements[(-1*ft_measurements[:,0]).argsort()]
            print(np.mean(ft_measurements[0:10, 1]))
    if is_fine_tuning:
        focus = measurements[ft_wb_i // fine_tuning_iterations, 1]
    else:
        focus = i
    if i % step_size == 0:
        os.system("v4l2-ctl -d %i -c focus_absolute=%i" % (dev, focus))
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    lpa = modified_laplace(gray)

    # Calc ROI focus:
    if not None in rect:
        x, y = rect[0], rect[1]
        w, h = rect[2], rect[3]
        cv2.rectangle(lpa, (x, y), (x+w, y+h),
                      (255, 255, 255), 5)
        if is_fine_tuning:
            ft_measurements.append([np.mean(lpa[y:y+h, x:x+w]), focus])
            print(np.mean(lpa[y:y+h, x:x+w]), focus)
        elif is_sweeping:
            measurements.append([np.mean(lpa[y:y+h, x:x+w]), focus])
            print(np.mean(lpa[y:y+h, x:x+w]), focus)
    cv2.imshow("Laplacian", lpa)
    k = chr(cv2.waitKey(2) & 0xFF)
    if k == "q":
        break
    if k == "j":
        i = (i+1) % max_focus
    if k == "k":
        i = (i-1) % max_focus
    if k == "m":
        i = 0
        measurements = []
        is_sweeping = True
cv2.destroyAllWindows()
