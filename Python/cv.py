#!/usr/bin/python

import cv2

def getPixel(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print "\nMouse trigger!"
        print "BGR: ",img[y,x]
        print "HSV: ",hsv[y,x]
    pass

img = cv2.imread('/root/iitm/1.png')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('img');
cv2.setMouseCallback('img',getPixel)
print "image shape: ", img.shape
print "image size: ", img.size

while True:
    cv2.imshow('img',img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
