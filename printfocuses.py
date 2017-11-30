import util
focuses = [util.focus_to_focal_length(i) for i in xrange(0, 255, 25)]
csv = "".join(["%i,\n" for i in focuses])
with open("focuses.csv", "w+") as f:
    f.write(csv)
