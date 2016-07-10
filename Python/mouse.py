#!/usr/bin/python

import cv2
import numpy as np

def drawCircle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),100,(255,0,0),-1)
    pass

img = np.zeros((512,512,3),np.uint8)
cv2.namedWindow('img');
cv2.setMouseCallback('img',drawCircle)

while True:
    cv2.imshow('img',img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
