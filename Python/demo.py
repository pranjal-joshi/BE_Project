#!/usr/bin/python

# A python script for image processing on IITM radar images
# Author    :   Pranjal P. Joshi
# Date      :   9 July 2016

import cv2
import numpy as np
import sys
import os

####### REQUIRED FUNCTIONS

def checkPath(path):
    if os.path.exists(path):
        return True
    else:
        return False

###### MAIN PROGRAM BEGINS FROM HERE!!

font = cv2.FONT_HERSHEY_SIMPLEX
path = "/root/iitm/1.png"
print "Opening image: ", path

if checkPath(path):
    img = cv2.imread(path)
else:
    sys.exit("Invalid image path is given!")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print "Converting source image to HSV and Grayscale...\n"

print "source image shape: ", img.shape
print "source image size: ", img.size

lower = np.array([10,220,172])
upper = np.array([40,239,212])

### HSV color boundaries ### #### CALIBRATE THIS VALUES USING CV.PY IF REQUIRED
cyan_lower = np.array([75,185,187])
cyan_upper = np.array([80,195,190])

red_mark_lower = np.array([0,255,255])
red_mark_upper = np.array([2,255,255])

blue_mark_lower = np.array([119,255,255])
blue_mark_upper = np.array([121,255,255])

sea_color_lower = np.array([90,223,133])
sea_color_upper = np.array([94,227,136])

light_green_lower = np.array([53,214,169])
light_green_upper = np.array([62,229,215])

yellow_lower = np.array([10,220,172])
yellow_upper = np.array([40,239,212])
############################

mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
res = cv2.bitwise_and(img, img, mask= mask)

blur = cv2.medianBlur(res,3)    #ODD values only for median filter

cv2.putText(img,'Original',(70,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
cv2.imshow('frame',img)
cv2.putText(mask,'Mask',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
cv2.imshow('mask',mask)
cv2.putText(res,'Processed',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
cv2.imshow('res',res)
cv2.putText(blur,'Filtered',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
cv2.imshow('blur',blur)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):                 ## exit loop on pressing Q key
        print "Quitting..."
        break
cv2.destroyAllWindows()
