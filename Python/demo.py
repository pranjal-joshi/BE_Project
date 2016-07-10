#!/usr/bin/python

import cv2
import numpy as np

img = cv2.imread('/root/iitm/1.png')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print "image shape: ", img.shape
print "image size: ", img.size

lower = np.array([90,250,130])
upper = np.array([95,255,139])

### HSV color boundaries ###
cyan_lower = np.array([80,205,193])
cyan_upper = np.array([92,210,197])
############################

mask = cv2.inRange(hsv, lower, upper)

res = cv2.bitwise_and(img, img, mask= mask)

cv2.imshow('frame',img)
cv2.imshow('mask',mask)
cv2.imshow('res',res)

while True:
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
