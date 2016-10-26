#!/usr/bin/python

import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import argparse
import os
import sys

t = time.time()

path = "/root/iitm/c1.png"
savePath = "/root/iitm/cloudTracking/"
AREAS = []

### CONSTANTS ###
STEPWISE = True
SHOW_IMAGES = False
STORE_ORIGNINAL_IMAGE = True
MINIMUM_CLOUD_AREA = 3000

'''
RADAR_START_POINT_X = 71 #253
RADAR_END_POINT_X = 1186 #1494
RADAR_RADIUS = 50 #125

PIXEL_X_SIDE = float(RADAR_RADIUS)/(RADAR_END_POINT_X - RADAR_START_POINT_X)

RADAR_START_POINT_Y = 1184 #1362
RADAR_END_POINT_Y = 68 #153
RADAR_HEIGHT = 15 #20

PIXEL_Y_SIDE = float(RADAR_HEIGHT)/(RADAR_START_POINT_Y - RADAR_END_POINT_Y)

PIXEL_AREA = float(PIXEL_Y_SIDE)*PIXEL_X_SIDE
'''
#################################################################

def checkPath(path):
	if os.path.exists(path):
		return True
	else:
		return False

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="Path to image")
ap.add_argument("-x","--diameter/radius",required=True,help="RADAR diameter in KM [ X axis ]")
ap.add_argument("-y","--height",required=True,help="RADAR height in KM [ Y axis ]")
args = vars(ap.parse_args())

path = args["image"]
RADAR_RADIUS = int(args["diameter/radius"])
RADAR_HEIGHT = int(args["height"])

print "Opening image: ", path

if checkPath(path):
    img = cv2.imread(path)
    outputImg = img
else:
    sys.exit("Invalid image path is given!")

## HSV white eliminate boundaries ##				## --> Remove white backgrounds
lower = np.array([0,52,0])
upper = np.array([180,255,255])

#background subtractor
bgsub = cv2.createBackgroundSubtractorMOG2()
bgmask = bgsub.apply(img)
r, bgmask = cv2.threshold(bgmask,127,255,cv2.THRESH_BINARY)
bgmaskImg = bgmask.copy()							## --> contour separation algorithm
_,bgmaskContours,_ = cv2.findContours(bgmaskImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

global leftmost
global rightmost
global topmost
global bottommost

for bgmaskCnt in bgmaskContours:
	global topmost
	global rightmost
	global leftmost
	global bottommost
	area = cv2.contourArea(bgmaskCnt)
	if area > 100000:
		leftmost = tuple(bgmaskCnt[bgmaskCnt[:,:,0].argmin()][0])
		rightmost = tuple(bgmaskCnt[bgmaskCnt[:,:,0].argmax()][0])
		topmost = tuple(bgmaskCnt[bgmaskCnt[:,:,1].argmin()][0])
		bottommost = tuple(bgmaskCnt[bgmaskCnt[:,:,1].argmax()][0])
		'''
		print "left " + str(leftmost)
		print "right " + str(rightmost)
		print "top " + str(topmost)
		print "bot " + str(bottommost)
		print area
		'''


RADAR_START_POINT_X = bottommost[0] #253
RADAR_END_POINT_X = rightmost[0] #1494
#RADAR_RADIUS = 50 #125

PIXEL_X_SIDE = float(RADAR_RADIUS)/(RADAR_END_POINT_X - RADAR_START_POINT_X)

RADAR_START_POINT_Y = bottommost[1] #1362
RADAR_END_POINT_Y = topmost[1] #153
#RADAR_HEIGHT = 15 #20

PIXEL_Y_SIDE = float(RADAR_HEIGHT)/(RADAR_START_POINT_Y - RADAR_END_POINT_Y)

PIXEL_AREA = float(PIXEL_Y_SIDE)*PIXEL_X_SIDE


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

print "\nAreas of all clouds (MINIMUM_CLOUD_AREA = %d pixels):\n" % MINIMUM_CLOUD_AREA

for cnt in contours:
	area = cv2.contourArea(cnt)
	if((area != 46368) and (area > MINIMUM_CLOUD_AREA) and (area != 62496)):		# exclude colorbar
		M = cv2.moments(cnt)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		outputImg = cv2.drawContours(img, contours, -1, (0,0,0), 3)
		cv2.circle(outputImg, (cX, cY), 4, (0,0,0), -1)
		printArea = (area*PIXEL_AREA)
		AREAS.append(round(printArea,5))
		printArea = ('%.3f' % printArea) + " Sq.Kms"				## truncate to 3 decimals
		print printArea
		cv2.putText(outputImg, printArea, (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50,50,50), 2)
	else:
		pass



if STEPWISE:
	k = cv2.imread(path)
	cv2.putText(k,'Source Image',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
	if STORE_ORIGNINAL_IMAGE:
		storePath = savePath + path + 'source.png'
		cv2.imwrite(storePath,k)

	cv2.putText(modifiedImg,'Background elimination',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
	storePath = savePath + path + 'noBackground.png'
	cv2.imwrite(storePath,modifiedImg)

	cv2.putText(gray_blur,'Grayscaled',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
	storePath = savePath + path + 'grayscale.png'
	cv2.imwrite(storePath,gray_blur)

	cv2.putText(thresh,'Adaptive thresholding',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
	storePath = savePath + path + 'thresholding.png'
	cv2.imwrite(storePath,thresh)

	cv2.putText(bgmask,'Grid subtraction',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
	storePath = savePath + path + 'grid.png'
	cv2.imwrite(storePath,bgmask)
	
	cv2.putText(outputImg,'Cloud Area',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
	tipText = "Scale: 1 pixel = " + str(PIXEL_AREA) + " Sq.Kms"
	cv2.putText(outputImg,tipText,(50,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
	storePath = savePath + path + 'output.png'
	cv2.imwrite(storePath,outputImg)

	'''print AREAS
	plt.plot(AREAS,'b--',AREAS,'rs')
	plt.show()'''

	if SHOW_IMAGES:
		cv2.imshow("Source Image",k)
		cv2.imshow("Background subtractor",bgmask)
		cv2.imshow("Background elimination",modifiedImg)
		cv2.imshow("Grayscale",gray_blur)
		cv2.imshow("Adaptive thresholding",thresh)
		cv2.imshow("Cloud Area",outputImg)

else:
	cv2.putText(outputImg,'Cloud Area',(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
	tipText = "Scale: 1 pixel = " + str(PIXEL_AREA) + " Sq.Kms"
	cv2.putText(outputImg,tipText,(50,75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
	cv2.imshow("Cloud Area",outputImg)
	storePath = savePath + path + 'output.png'
	cv2.imwrite(storePath,outputImg)

#print "\nTime required for script execution: "+str(round(time.time()-t,3))+" Seconds\n"

if SHOW_IMAGES:
	while True:
	    key = cv2.waitKey(1) & 0xFF
	    if key == ord("q"):                 ## exit loop on pressing Q key
	        print "\nQuitting..."
	        break

	cv2.destroyAllWindows()