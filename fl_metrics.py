import os
import itertools
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

labels_loc = r"C:\Users\u15013121\Desktop\JP\Forklift-Object-detection\yolov5\runs\detect\exp12\labels"
labels = glob(f"{labels_loc}/*")

#define Matplotlib figure and axis
fig, ax = plt.subplots()

#create simple line plot
# ax.plot([0, 10],[0, 10])
box_centers = []
bb_1 = None
direction_1 = None
speed_1 = None
direction = None
speed = None
k = 0.5
forklift_width = 1
forklift_height = 2 # in meters
frame_rate = 1 # in seconds
mps_to_kph = 3.6 #multiply meter per second by this to get kilometer per hour
metrics = {}

def intersection_over_union(box1, box2):
    # Extract the coordinates and dimensions of each box
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Calculate the coordinates of the intersection rectangle
    x_inter1 = max(x1, x2)
    y_inter1 = max(y1, y2)
    x_inter2 = min(x1 + w1, x2 + w2)
    y_inter2 = min(y1 + h1, y2 + h2)

    # Calculate the area of the intersection rectangle
    inter_width = max(0, x_inter2 - x_inter1)
    inter_height = max(0, y_inter2 - y_inter1)
    inter_area = inter_width * inter_height

    # Calculate the area of both bounding boxes
    box1_area = w1 * h1
    box2_area = w2 * h2

    # Calculate the IoU
    union_area = box1_area + box2_area - inter_area
    iou = inter_area / union_area

    return iou

def get_bb_center(bb):
    x, y, w, h = bb
    cx = x + 0.5*w
    cy = y + 0.5*h
    return cx, cy, w, h


def calc_speed(bb, bb_1):
    cx, cy, h, w = get_bb_center(bb)
    cx_1, cy_1, h_1, w_1 = get_bb_center(bb_1)

    direction = "left" if (cx < cx_1) else "right"

    loc_change = np.sqrt((cx - cx_1)**2 + (cy - cy_1)**2)
    bb_size = h*w_1
    bb_size_1 = h_1*w_1
    bb_size_change = bb_size/bb_size_1
    bb_size_change = 1/bb_size_change if bb_size_change < 1 else bb_size_change

    meters_per_pixel = h/forklift_height
    meter_change = (loc_change  * bb_size_change) * meters_per_pixel 
    speed = (meter_change/frame_rate)*mps_to_kph

    return direction, speed

def detect_significant_events(direction, direction_1, speed, speed_1):
    #Assuming speed is in kph
    speed = speed if speed > 1 else 0
    speed_1 = speed_1 if speed_1 > 1 else 0
    if direction !=  direction_1 and (speed > 0 or speed_1 > 0):
        print(f"Forklift changes direction from {direction_1} to {direction}!!")
    if speed > 10:
        print(f"Forklift is moving fast at {speed} kph!!")
    if abs(speed - speed_1) > 5:
        print(f"Sudden change in speed detected!!")

def detect_possible_colision(bbs):
    if len(bbs) > 1:
        for bb1, bb2 in itertools.combinations(bbs, 2):
            if intersection_over_union(bb1, bb2) > 0.3:
                print("Possible collision detected!!")
            

i = 0
for label in labels:
    f = open(label, "r")
    points = f.read()
    bbs = []
    j = 0
    for point in points.splitlines():
        l, x, y, w, h = point.split(" ")
        x, y, w, h = float(x), float(y), float(w), float(h)
        bb = [x, y, w, h]
        bbs.append(bb)

        #add rectangle to plot
        # ax.add_patch(Rectangle((x, y), w, h, fill=False))
        # plt.scatter(cx, cy)
        # box_centers.append((cx, cy))
        if bb_1:
            direction, speed = calc_speed(bb, bb_1)
    detect_possible_colision(bbs)
    if all([direction_1, speed_1]):
        detect_significant_events(direction, direction_1, speed, speed_1)

    bb_1 = bb
    if all([direction, speed]):
        direction_1 = direction
        speed_1 = speed
        
      
#display plot
# plt.show()

# dists = []
# for i in range(len(box_centers)):
#     dist = (box_centers[i-1][0] - box_centers[i][0])**2 
#     dist += (box_centers[i-1][1] - box_centers[i][1])**2
#     dist = np.sqrt(dist)
#     dists.append(dist)
# # print(box_centers)
# print(dists)

# print(metrics)