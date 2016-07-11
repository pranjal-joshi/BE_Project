#!/usr/bin/python

import cv2
import sys
import os

def checkPath(path):
    if os.path.exists(path):
        return True
    else:
        return False

def getPixel(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print "\nMouse trigger!"
        print "BGR: ",img[y,x]
        print "HSV: ",hsv[y,x]
    pass

path = '/root/iitm/1.png'

if checkPath(path):
    img = cv2.imread(path)
else:
    sys.exit("Image path not found!!")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('img',cv2.WINDOW_AUTOSIZE);
cv2.setMouseCallback('img',getPixel)
print "image shape: ", img.shape
print "image size: ", img.size

while True:
    cv2.imshow('img',img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):                 ## exit loop on pressing Q key
        break
cv2.destroyAllWindows()
