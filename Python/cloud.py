#!/usr/bin/python

# Author: Pranjal Joshi
# Date 	: 24-10-2016
# Script to calculate cloud area using image processing.

import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import argparse
import os
import sys
import imutils

path = "/home/cyberfox/iitm/c1.png"
savePath = "/home/cyberfox/iitm/cloudTracking/"
AREAS = []

### CONSTANTS ###
STEPWISE = True
SHOW_IMAGES = False
STORE_ORIGNINAL_IMAGE = False
MINIMUM_CLOUD_AREA = 2000

# Reflectivity values
COLORBAR = [-32,-28,-24,-16,-12,-8,-4,0,8,12,16,24,28,32,40]

# HSV color ranges
COLOR_HSV_ARRAY = [np.array([120,255,255]),
					np.array([90,255,255]),
					np.array([75,255,255]),
					np.array([60,255,255]),
					np.array([60,255,175]),
					np.array([70,255,150]),
					np.array([30,255,255]),
					np.array([24,255,255]),
					np.array([20,255,255]),
					np.array([10,255,255]),
					np.array([0,255,255]),
					np.array([168,255,255]),
					np.array([150,255,255]),
					np.array([150,127,255]),
					np.array([150,52,255])
					]
#################################################################

def checkPath(path):	# check for valid path
	if os.path.exists(path):
		return True
	else:
		return False

def sortContours(cnt):	# sort from left-to-right
	reverseSort = True
	boundingBoxes = [cv2.boundingRect(c) for c in cnt]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnt, boundingBoxes),key=lambda b:b[1][0], reverse=reverseSort))
	return (cnts, boundingBoxes)

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="Path to image")
ap.add_argument("-x","--diameter",required=True,help="RADAR diameter in KM [ X axis ]")
ap.add_argument("-y","--height",required=True,help="RADAR height in KM [ Y axis ]")
ap.add_argument("-l","--lower",required=False,help="Lower range of Reflectivity")
ap.add_argument("-u","--upper",required=False,help="Upper range of Reflectivity")
args = vars(ap.parse_args())

path = args["image"]
RADAR_DIAMETER = int(args["diameter"])
RADAR_HEIGHT = int(args["height"])
lowerRange = int(args["lower"])
upperRange = int(args["upper"])
rangeScale = "Reflectivity range: " + str(lowerRange) + " to " + str(upperRange) + " (in dB)"

print "\nOpening image: ", path

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


RADAR_START_POINT_X = bottommost[0] #253
RADAR_END_POINT_X = rightmost[0] #1494

PIXEL_X_SIDE = float(RADAR_DIAMETER)/(RADAR_END_POINT_X - RADAR_START_POINT_X)

RADAR_START_POINT_Y = bottommost[1] #1362
RADAR_END_POINT_Y = topmost[1] #153

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

########################## NEW CODE - 18 Jan
if(lowerRange != None and upperRange != None):
	try:
		lowerIndex = COLORBAR.index(lowerRange)
		upperIndex = COLORBAR.index(upperRange)
		if(upperRange < lowerRange):
			sys.exit("Upper range can't be smaller than lower range!")
	except Exception as e:
		print "Given color value is not in range!\nColor Ranges ->" + str(COLORBAR)
		sys.exit(0)
	### for entire image
	loopCount = len(COLORBAR)-1
	offsetCount = 0
	outerMask = np.zeros((img.shape[0],img.shape[1]),np.uint8)
	for j in range(0,loopCount+1):
		outerMaskTemp = cv2.inRange(hsvImg, COLOR_HSV_ARRAY[offsetCount], COLOR_HSV_ARRAY[offsetCount])
		offsetCount = offsetCount + 1
		outerMask = outerMaskTemp + outerMask
	outerRegion = cv2.bitwise_and(modifiedImg,modifiedImg, mask=outerMask)

	### for entire image - eliminate outer part
	loopCount = lowerIndex
	offsetCount = 0
	outerMask2 = np.zeros((img.shape[0],img.shape[1]),np.uint8)
	for j in range(0,loopCount+1):
		outerMaskTemp = cv2.inRange(hsvImg, COLOR_HSV_ARRAY[offsetCount], COLOR_HSV_ARRAY[offsetCount])
		offsetCount = offsetCount + 1
		outerMask2 = outerMaskTemp + outerMask2
	outerRegion2 = cv2.bitwise_and(modifiedImg,modifiedImg, mask=outerMask2)

	### for ranged region
	loopCount = upperIndex - lowerIndex
	offsetCount = lowerIndex
	colorMask = np.zeros((img.shape[0],img.shape[1]),np.uint8)
	for j in range(0,loopCount+1):
		colorMaskTemp = cv2.inRange(hsvImg, COLOR_HSV_ARRAY[offsetCount], COLOR_HSV_ARRAY[offsetCount])
		offsetCount = offsetCount + 1
		colorMask = colorMask + colorMaskTemp
	rangedImage = cv2.bitwise_and(modifiedImg,modifiedImg, mask=colorMask)

	### for innermost image - inner part elimination
	loopCount = (len(COLORBAR)-1) - upperIndex
	offsetCount = upperIndex+1
	innerMask = np.zeros((img.shape[0],img.shape[1]),np.uint8)
	for j in range(0,loopCount):
		innerMaskTemp = cv2.inRange(hsvImg, COLOR_HSV_ARRAY[offsetCount], COLOR_HSV_ARRAY[offsetCount])
		offsetCount = offsetCount + 1
		innerMask = innerMaskTemp + innerMask
	innerRegion = cv2.bitwise_and(modifiedImg,modifiedImg, mask=innerMask)

	requiredRegionMask = cv2.bitwise_xor(outerMask, innerMask)
	requiredRegionMask = cv2.bitwise_xor(requiredRegionMask, outerMask2)
	rangedNew = cv2.bitwise_and(modifiedImg, modifiedImg, mask=requiredRegionMask)
	rangedImage = rangedNew

##########################

# Graysacale original image		 					## --> Convert masked image to grayscale
grayImg = cv2.cvtColor(rangedImage,cv2.COLOR_BGR2GRAY)
gray_blur = grayImg
innerGray = cv2.cvtColor(innerRegion,cv2.COLOR_BGR2GRAY)
outerGray = cv2.cvtColor(outerRegion,cv2.COLOR_BGR2GRAY)
#gray_blur = cv2.GaussianBlur(grayImg, (3,3), 0)	## <-- Deprecated.This reduces precesion.

## --> Thresholding. convert to binary image.
thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 3, 1)
innerThresh = cv2.adaptiveThreshold(innerGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 3, 1)
outerThresh = cv2.adaptiveThreshold(outerGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 3, 1)

contourImg = thresh.copy()							## --> contour separation algorithm
_,contours,_ = cv2.findContours(contourImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
(contours, boundingBoxes) = sortContours(contours)
colorBoxContour = contours[0]
contours = contours[1:len(contours)]				## --> Exclude color bar area calculations :)

print "\nAreas of all clouds (MINIMUM_CLOUD_AREA = %d pixels):\n" % MINIMUM_CLOUD_AREA
contourCounter = 0

for cnt in contours:
	area = cv2.contourArea(cnt)
	if(area > MINIMUM_CLOUD_AREA):
		M = cv2.moments(cnt)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		#### new code - 29 JAN - cloud cropping & thresholding ###
		x,y,w,h = cv2.boundingRect(cnt)
		cv2.rectangle(outputImg,(x,y),(x+w,y+h),(0,0,255),3)
		croppedCloud = gray_blur[y:y+h, x:x+w]
		ret,croppedCloudThresh = cv2.threshold(croppedCloud,1,255,cv2.THRESH_BINARY)
		area = cv2.countNonZero(croppedCloudThresh)
		####
		outputImg = cv2.drawContours(img, contours, -1, (0,0,0), 3)
		cv2.circle(outputImg, (cX, cY), 4, (0,0,0), -1)
		printArea = (area*PIXEL_AREA)
		AREAS.append(round(printArea,5))
		printArea = ('%.3f' % printArea) + " Sq.Kms "				## truncate to 3 decimals
		contourCounter = contourCounter + 1
		print printArea + "\t-> cloud number ->\t" + str(contourCounter)
		cv2.putText(outputImg, printArea, (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20,20,20), 2)
		try:
			cv2.putText(outputImg, str(contourCounter), (x+w-10,y-20),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
		except Exception as e:
			pass
	else:
		pass

contours = list(contours)
contours.insert(0, colorBoxContour)
contours = tuple(contours)
outputImg = cv2.drawContours(outputImg, contours, -1,(0,0,0),3)

innerCopy = innerThresh.copy()
_,innerContours,_ = cv2.findContours(innerCopy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
(innerContours, boundingBoxes) = sortContours(innerContours)
innerContours = innerContours[1:len(innerContours)]

for c in innerContours:
	outputImg = cv2.drawContours(outputImg, innerContours, -1, (0,0,0), 2)
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

	cv2.putText(outputImg,'Cloud Area',(75,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
	tipText = "Scale: 1 pixel = " + str(PIXEL_AREA) + " Sq.Kms"
	cv2.putText(outputImg,tipText,(75,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
	cv2.putText(outputImg,rangeScale,(75,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
	storePath = savePath + path + 'output.png'
	cv2.imwrite(storePath,outputImg)

	if SHOW_IMAGES:
		cv2.imshow("Source Image",k)
		cv2.imshow("Background subtractor",bgmask)
		cv2.imshow("Background elimination",modifiedImg)
		cv2.imshow("Grayscale",gray_blur)
		cv2.imshow("Adaptive thresholding",thresh)
		cv2.imshow("Cloud Area",outputImg)
		cv2.imshow("Color Range image",rangedImage)
		cv2.imshow("InnerMask",innerRegion)
		cv2.imshow("OuterRegion",outerRegion)
		cv2.imshow("Color RangeNew image",rangedNew)
		cv2.imshow("Cropped cloud",croppedCloud)
		cv2.imshow("croppedThresh",croppedCloudThresh)

else:
	cv2.putText(outputImg,'Cloud Area',(75,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
	tipText = "Scale: 1 pixel = " + str(PIXEL_AREA) + " Sq.Kms"
	cv2.putText(outputImg,tipText,(75,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
	cv2.putText(outputImg,rangeScale,(75,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
	storePath = savePath + path + 'output.png'
	cv2.imwrite(storePath,outputImg)

if SHOW_IMAGES:
	while True:
	    key = cv2.waitKey(1) & 0xFF
	    if key == ord("q"):                 ## exit loop on pressing Q key
	        print "\nQuitting..."
	        break

	cv2.destroyAllWindows()
