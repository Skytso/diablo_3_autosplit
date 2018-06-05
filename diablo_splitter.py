# Importing the libraries needed
import cv2
import mss
import mss.tools
import numpy as np
from matplotlib import pyplot as plt
import socket

# List of split images to compare
split_template = [
        'images/diablo_act1.png',
        'images/diablo_act2.png',
        'images/diablo_act3.png',
        'images/diablo_act4.png',
        'images/diablo_run.png'
    ]

regions = [
    {'top': 0, 'left': 0, 'width': 1920, 'height': 1080},
    {'top': 0, 'left': 0, 'width': 1920, 'height': 1080},
    {'top': 0, 'left': 0, 'width': 1920, 'height': 1080},
    {'top': 0, 'left': 0, 'width': 1920, 'height': 1080},
    {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
    ]

split_num = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(("localhost", 16834))
except socket.error as exc:
    print("Caught exception socket.error : %s" % exc)
    print("Ensure LiveSplit's Server Component is enabled.")

# Load images into the list
for i in range(len(split_template)):
    template = cv2.imread(split_template[i])
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    split_template[i] = template

# Screenshot function ouput to 'compare.png'
def capture(region):
    img = np.array(mss.mss().grab(region))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

# Comparison function
def compare(template, screen):
    method = eval('cv2.TM_CCOEFF_NORMED')
    res = cv2.matchTemplate(screen, template, method)
    min, max, loc1, loc2 = cv2.minMaxLoc(res)
    if max > .8:
        return True # images match
    else:
        return False # images don't match

# Main loop
while (split_num < len(split_template)):
    if compare(split_template[split_num], capture(regions[split_num])):
        s.send(b"startorsplit\r\n") #trigger the split
        split_num += 1
        print("Split triggered: " + str(split_num))

print("Run ended.")
