#!/usr/bin/python

# A python script for image processing on IITM radar images
# Author    :   Pranjal P. Joshi
# Date      :   9 July 2016

import cv2
import numpy as np
import sys
import os
from time import sleep
import argparse

####### REQUIRED FUNCTIONS

def checkPath(path):
    if os.path.exists(path):
        return True
    else:
        return False

###### MAIN PROGRAM BEGINS FROM HERE!!

print "\n"
font = cv2.FONT_HERSHEY_SIMPLEX
ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="Path to image")
args = vars(ap.parse_args())
path = args["image"]
print "Opening image: ", path

if checkPath(path):
    img = cv2.imread(path)
else:
    sys.exit("Invalid image path is given!")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print "Converting source image to HSV and Grayscale...\n"

print "source image shape: ", img.shape
print "source image size: ", img.size,"\n"

lower = np.array([10,220,172])
upper = np.array([40,239,212])

### HSV color boundaries ### #### CALIBRATE THIS VALUES USING CV.PY IF REQUIRED
cyan_lower = np.array([80,195,190])
cyan_upper = np.array([95,210,200])

red_mark_lower = np.array([0,255,255])
red_mark_upper = np.array([2,255,255])

blue_mark_lower = np.array([119,255,255])
blue_mark_upper = np.array([121,255,255])

sea_color_lower = np.array([90,223,133])
sea_color_upper = np.array([94,227,136])

light_green_lower = np.array([53,214,169])
light_green_upper = np.array([62,229,215])

dark_green_lower = np.array([55,175,125])
dark_green_upper = np.array([65,225,150])

yellow_lower = np.array([10,220,172])
yellow_upper = np.array([40,239,212])
############################

savePath = str('/root/iitm/cv_out/original'+path+'.png')
cv2.imwrite(savePath,img)

### Cyan color separation routine ####
cyan_mask = cv2.inRange(hsv, cyan_lower, cyan_upper)
cyan_res = cv2.bitwise_and(img, img, mask= cyan_mask)
pix = cv2.countNonZero(cyan_mask)
totalPix = cv2.countNonZero(grayimg);
pixelArea = "Pixel area of Cyan: \t\t" + str(float(pix)/totalPix*100.0) + "% [" + str(pix) + "/"+ str(totalPix) + " pix/image]"
print pixelArea
cyan_blur = cv2.medianBlur(cyan_res,3)    #ODD values only for median filter
cv2.putText(img,'Original',(70,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('frame',img)
cv2.putText(cyan_mask,'CyanMask',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('mask',cyan_mask)
cv2.putText(cyan_res,'CyanProcessed',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('res',cyan_res)
cv2.putText(cyan_blur,'CyanFiltered',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('blur',cyan_blur)
savePath = str('/root/iitm/cv_out/'+path+'cyan.png')
cv2.imwrite(savePath,cyan_res)
savePath = str('/root/iitm/cv_out/'+path+'CyanFiltered.png')
cv2.imwrite(savePath,cyan_blur)
### Cyan sepearation ends here ###

### yellow color separation routine ####
yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
yellow_res = cv2.bitwise_and(img, img, mask= yellow_mask)
pix = cv2.countNonZero(yellow_mask)
totalPix = cv2.countNonZero(grayimg);
pixelArea = "Pixel area of yellow: \t\t" + str(float(pix)/totalPix*100.0) + "% [" + str(pix) + "/"+ str(totalPix) + " pix/image]"
print pixelArea
yellow_blur = cv2.medianBlur(yellow_res,3)    #ODD values only for median filter
cv2.putText(img,'Original',(70,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('frame',img)
cv2.putText(yellow_mask,'yellowMask',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('mask',yellow_mask)
cv2.putText(yellow_res,'yellowProcessed',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('res',yellow_res)
cv2.putText(yellow_blur,'yellowFiltered',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('blur',yellow_blur)
savePath = str('/root/iitm/cv_out/'+path+'yellow.png')
cv2.imwrite(savePath,yellow_res)
savePath = str('/root/iitm/cv_out/'+path+'YellowFiltered.png')
cv2.imwrite(savePath,yellow_blur)
### yellow sepearation ends here ###

### red_mark color separation routine ####
red_mark_mask = cv2.inRange(hsv, red_mark_lower, red_mark_upper)
red_mark_res = cv2.bitwise_and(img, img, mask= red_mark_mask)
pix = cv2.countNonZero(red_mark_mask)
totalPix = cv2.countNonZero(grayimg);
pixelArea = "Pixel area of red_mark: \t" + str(float(pix)/totalPix*100.0) + "% [" + str(pix) + "/"+ str(totalPix) + " pix/image]"
print pixelArea
red_mark_blur = cv2.medianBlur(red_mark_res,3)    #ODD values only for median filter
cv2.putText(img,'Original',(70,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('frame',img)
cv2.putText(red_mark_mask,'red_markMask',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('mask',red_mark_mask)
cv2.putText(red_mark_res,'red_markProcessed',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('res',red_mark_res)
cv2.putText(red_mark_blur,'red_markFiltered',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('blur',red_mark_blur)
savePath = str('/root/iitm/cv_out/'+path+'red_mark.png')
cv2.imwrite(savePath,red_mark_res)
### red_mark sepearation ends here ###

### blue_mark color separation routine ####
blue_mark_mask = cv2.inRange(hsv, blue_mark_lower, blue_mark_upper)
blue_mark_res = cv2.bitwise_and(img, img, mask= blue_mark_mask)
pix = cv2.countNonZero(blue_mark_mask)
totalPix = cv2.countNonZero(grayimg);
pixelArea = "Pixel area of blue_mark: \t" + str(float(pix)/totalPix*100.0) + "% [" + str(pix) + "/"+ str(totalPix) + " pix/image]"
print pixelArea
blue_mark_blur = cv2.medianBlur(blue_mark_res,3)    #ODD values only for median filter
cv2.putText(img,'Original',(70,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('frame',img)
cv2.putText(blue_mark_mask,'blue_markMask',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('mask',blue_mark_mask)
cv2.putText(blue_mark_res,'blue_markProcessed',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('res',blue_mark_res)
cv2.putText(blue_mark_blur,'blue_markFiltered',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('blur',blue_mark_blur)
savePath = str('/root/iitm/cv_out/'+path+'blue_mark.png')
cv2.imwrite(savePath,blue_mark_res)
### blue_mark sepearation ends here ###

### sea_color color separation routine ####
sea_color_mask = cv2.inRange(hsv, sea_color_lower, sea_color_upper)
sea_color_res = cv2.bitwise_and(img, img, mask= sea_color_mask)
pix = cv2.countNonZero(sea_color_mask)
totalPix = cv2.countNonZero(grayimg);
pixelArea = "Pixel area of sea_color: \t" + str(float(pix)/totalPix*100.0) + "% [" + str(pix) + "/"+ str(totalPix) + " pix/image]"
print pixelArea
sea_color_blur = cv2.medianBlur(sea_color_res,3)    #ODD values only for median filter
cv2.putText(img,'Original',(70,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('frame',img)
cv2.putText(sea_color_mask,'sea_colorMask',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('mask',sea_color_mask)
cv2.putText(sea_color_res,'sea_colorProcessed',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('res',sea_color_res)
cv2.putText(sea_color_blur,'sea_colorFiltered',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('blur',sea_color_blur)
savePath = str('/root/iitm/cv_out/'+path+'sea_color.png')
cv2.imwrite(savePath,sea_color_res)
### sea_color sepearation ends here ###

### light_green color separation routine ####
light_green_mask = cv2.inRange(hsv, light_green_lower, light_green_upper)
light_green_res = cv2.bitwise_and(img, img, mask= light_green_mask)
pix = cv2.countNonZero(light_green_mask)
totalPix = cv2.countNonZero(grayimg);
pixelArea = "Pixel area of light_green: \t" + str(float(pix)/totalPix*100.0) + "% [" + str(pix) + "/"+ str(totalPix) + " pix/image]"
print pixelArea
light_green_blur = cv2.medianBlur(light_green_res,3)    #ODD values only for median filter
cv2.putText(img,'Original',(70,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('frame',img)
cv2.putText(light_green_mask,'light_greenMask',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('mask',light_green_mask)
cv2.putText(light_green_res,'light_greenProcessed',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('res',light_green_res)
cv2.putText(light_green_blur,'light_greenFiltered',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('blur',light_green_blur)
savePath = str('/root/iitm/cv_out/'+path+'light_green.png')
cv2.imwrite(savePath,light_green_res)
savePath = str('/root/iitm/cv_out/'+path+'LightGreenFiltered.png')
cv2.imwrite(savePath,light_green_blur)
### light_green sepearation ends here ###

### dark_green color separation routine ####
dark_green_mask = cv2.inRange(hsv, dark_green_lower, dark_green_upper)
dark_green_res = cv2.bitwise_and(img, img, mask= dark_green_mask)
pix = cv2.countNonZero(dark_green_mask)
totalPix = cv2.countNonZero(grayimg);
pixelArea = "Pixel area of dark_green: \t" + str(float(pix)/totalPix*100.0) + "% [" + str(pix) + "/"+ str(totalPix) + " pix/image]"
print pixelArea
dark_green_blur = cv2.medianBlur(dark_green_res,3)    #ODD values only for median filter
cv2.putText(img,'Original',(70,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('frame',img)
cv2.putText(dark_green_mask,'dark_greenMask',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('mask',dark_green_mask)
cv2.putText(dark_green_res,'dark_greenProcessed',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('res',dark_green_res)
cv2.putText(dark_green_blur,'dark_greenFiltered',(50,50), font, 1, (255,255,255), 2, cv2.LINE_AA)
#cv2.imshow('blur',dark_green_blur)
savePath = str('/root/iitm/cv_out/'+path+'dark_green.png')
cv2.imwrite(savePath,dark_green_res)
savePath = str('/root/iitm/cv_out/'+path+'DarkGreenFiltered.png')
cv2.imwrite(savePath,dark_green_blur)
### dark_green sepearation ends here ###

"""while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):                 ## exit loop on pressing Q key
        print "\nQuitting..."
        break"""
cv2.destroyAllWindows()
print "\n"
