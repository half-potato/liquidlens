import sys, os, cv2

source = sys.argv[1]
dest = sys.argv[2]

if not os.path.isdir(dest):
    os.mkdir(dest)

files = [name for name in os.listdir(source) if os.path.isfile(os.path.join(source, name)) and "image" in name]

for i in files:
    img = cv2.imread(os.path.join(source, i))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(dest, i), gray)
