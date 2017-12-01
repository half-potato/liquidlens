import cv2
import signal

# Patience is in seconds. Lower if camera refused to open
def openCamera(dev, patience=5):
    cap = cv2.VideoCapture(dev)
    cap.set(3, 640)
    cap.set(4, 480)

    def handler(signum, frame):
        a = 1
        raise Exception("Camera timed out")

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(5)
    try:
        ret, frame = cap.read()
        signal.pause()
    except:
        print("Camera timed out using custom timeout")

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
    return cap

def focus_to_focal_length(f):
    if f == 0:
        f = 0.5
    return 165470*float(f)**(-2.55)
