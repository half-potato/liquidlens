import util
focuses = [util.focus_to_focal_length(i) for i in xrange(10, 255, 5)]
csv = "".join(["%f,\n" % i for i in focuses])
with open("focuses.csv", "w+") as f:
    f.write(csv)
