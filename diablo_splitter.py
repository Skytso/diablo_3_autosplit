# Importing the libraries needed
import sys
import cv2
import mss
import mss.tools
import numpy as np
from matplotlib import pyplot as plt
import socket

# List of split images to compare
split_template = [
        'images/1-skeleton_king.png',
        'images/2-araneae.png',
        'images/3-butcher.png',
        'images/4-act1.png',
        'images/5-maghda.png',
        'images/6-zoltun_kulle.png',
        'images/7-belial.png',
        'images/8-act2.png',
        'images/9-ghom.png',
        'images/10-siegebreaker.png',
        'images/11-cydaea.png',
        'images/12-azmodan.png',
        'images/13-act3.png',
        'images/14-iskatu.png',
        'images/15-rakanoth.png',
        'images/16-izual.png',
        'images/17-act4.png',
        'images/18-urzael.png',
        'images/19-adria.png',
        'images/20-end.png',
    ]

# List of regions for each image
regions = [
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #1
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #2
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #3
    {'top': 0, 'left': 1220, 'width': 700, 'height': 400},      #4
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #5
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #6
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #7
    {'top': 0, 'left': 1220, 'width': 700, 'height': 400},      #8
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #9
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #10
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #11
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #12
    {'top': 0, 'left': 1220, 'width': 700, 'height': 400},      #13
    {'top': 730, 'left': 700, 'width': 700, 'height': 400},     #14
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #15
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #16
    {'top': 0, 'left': 1220, 'width': 700, 'height': 400},      #17
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #18
    {'top': 285, 'left': 1220, 'width': 700, 'height': 400},    #19
    {'top': 730, 'left': 700, 'width': 700, 'height': 400},     #20
    ]

# Set starting split
split_num = 0

# Wait for keypress to start
# Print instructions, splits, and commands
print(" Make sure LiveSplit's Server Component is enabled.")
print(" To reset or exit, simply close this window.")
input(" Press Enter to continue... \n")
print(" The splits are as follows:")
for i in range(len(split_template)):
    string = split_template[i]
    string = string.split(".png")[0]
    string = string.split("-", 1)[1]
    print("  " + str(i + 1) + " " + string)
input(" Press Enter to start... \n")

# Connect to Livesplit's socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(("localhost", 16834))
except socket.error as exc:
    sys.exit("Could not connect to Livesplit. Ensure LiveSplit's Server Component is enabled.")

print(" Autosplit started. Don't forget to start your timer normally! \n")

# Load images into the list0
for i in range(len(split_template)):
    template = cv2.imread(split_template[i])
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    split_template[i] = template

# Capture part of the screen
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
        s.send(b"startorsplit\r\n") # trigger the split
        split_num += 1
        print("Split triggered: " + str(split_num))

print("Run ended.")
