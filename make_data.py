import os
from glob import glob

prediction_location = r"C:\Users\u15013121\Desktop\JP\Forklift-Object-detection\yolov5\runs\detect\exp13\labels"
labels = glob(f"{prediction_location}/*")

i = 0

for label in labels:
    f = open(label, "r")
    points = f.read()
    for point in points.splitlines():
        l, x, y, w, h = point.split(" ")
        print(i)
        i += 1