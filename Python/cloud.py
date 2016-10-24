#!/usr/bin/python

import cv2
import numpy as np
import time

t = time.time()

path = "/root/iitm/cloud.png"
savePath = "/root/iitm/cloudTracking/"

### CONSTANTS ###
STEPWISE = True
SHOW_IMAGES = False
STORE_ORIGNINAL_IMAGE = True

RADAR_START_POINT_X = 253
RADAR_END_POINT_X = 1494
RADAR_RADIUS = 125

PIXEL_X_SIDE = float(RADAR_RADIUS)/(RADAR_END_POINT_X - RADAR_START_POINT_X)

RADAR_START_POINT_Y = 1362
RADAR_END_POINT_Y = 153
RADAR_HEIGHT = 20

PIXEL_Y_SIDE = float(RADAR_HEIGHT)/(RADAR_START_POINT_Y - RADAR_END_POINT_Y)

PIXEL_AREA = float(PIXEL_Y_SIDE)*PIXEL_X_SIDE

#################################################################

## HSV white eliminate boundaries ##				## --> Remove white backgrounds
lower = np.array([0,52,0])
upper = np.array([180,255,255])

# read image
img = cv2.imread(path)
outputImg = img

# HSV cloud separation								## --> Convert to HSV colorspace
hsvImg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsvImg, lower, upper)

# erodsion											## --> Morphological erosion & dilation to remove markings plotted on the image.
erodeMask = np.ones((5,5), np.uint8)
erodedImg = cv2.erode(mask, erodeMask, iterations=1)

# dialation
dilateMask = np.ones((5,5), np.uint8)
dilatedImg = cv2.dilate(erodedImg, dilateMask, iterations=1)

modifiedImg = cv2.bitwise_and(img,img, mask=dilatedImg)		## --> Mask hsv colorspace with original image. cloud separated from background.

# Graysacale original image		 					## --> Convert masked image to grayscale
grayImg = cv2.cvtColor(modifiedImg,cv2.COLOR_BGR2GRAY)
gray_blur = grayImg
#gray_blur = cv2.GaussianBlur(grayImg, (3,3), 0)	## <-- Deprecated.This reduces precesion.

## --> Thresholding. convert to binary image.
thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 3, 1)

contourImg = thresh.copy()							## --> contour separation algorithm
_,contours,_ = cv2.findContours(contourImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print "Areas of all contours:\n"

for cnt in contours:
	area = cv2.contourArea(cnt)
	if((area != 46368) and (area > 200)):
		M = cv2.moments(cnt)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		outputImg = cv2.drawContours(img, contours, -1, (0,0,0), 3)
		cv2.circle(outputImg, (cX, cY), 4, (0,0,0), -1)
		printArea = (area*PIXEL_AREA)
		printArea = ('%.3f' % printArea) + " Sq.Kms"				## truncate to 3 decimals
		print printArea
		cv2.putText(outputImg, printArea, (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,50,50), 2)
	else:
		pass


if STEPWISE:
	k = cv2.imread(path)
	cv2.putText(k,'Source Image',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
	if STORE_ORIGNINAL_IMAGE:
		storePath = savePath + 'source.png'
		cv2.imwrite(storePath,k)

	cv2.putText(modifiedImg,'Background elimination',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
	storePath = savePath + 'noBackground.png'
	cv2.imwrite(storePath,modifiedImg)

	cv2.putText(gray_blur,'Grayscaled',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
	storePath = savePath + 'grayscale.png'
	cv2.imwrite(storePath,gray_blur)

	cv2.putText(thresh,'Adaptive thresholding',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
	storePath = savePath + 'thresholding.png'
	cv2.imwrite(storePath,thresh)
	
	cv2.putText(outputImg,'Cloud Area',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
	tipText = "Scale: 1 pixel = " + str(PIXEL_AREA) + " Sq.Kms"
	cv2.putText(outputImg,tipText,(50,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
	storePath = savePath + 'output.png'
	cv2.imwrite(storePath,outputImg)

	if SHOW_IMAGES:
		cv2.imshow("Source Image",k)
		cv2.imshow("Background elimination",modifiedImg)
		cv2.imshow("Grayscale",gray_blur)
		cv2.imshow("Adaptive thresholding",thresh)
		cv2.imshow("Cloud Area",outputImg)
else:
	cv2.putText(outputImg,'Cloud Area',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
	tipText = "Scale: 1 pixel = " + str(PIXEL_AREA) + " Sq.Kms"
	cv2.putText(outputImg,tipText,(50,75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
	cv2.imshow("Cloud Area",outputImg)
	storePath = savePath + 'output.png'
	cv2.imwrite(storePath,outputImg)

print "\nTime required for script execution: "+str(round(time.time()-t,3))+" Seconds\n"

if SHOW_IMAGES:
	while True:
	    key = cv2.waitKey(1) & 0xFF
	    if key == ord("q"):                 ## exit loop on pressing Q key
	        print "\nQuitting..."
	        break

	cv2.destroyAllWindows()