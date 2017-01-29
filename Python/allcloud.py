#!/usr/bin/python

# Author: Pranjal Joshi
# Date 	: 26-10-2016

import os
import sys
import argparse
import time

# Place input images in this dirctory.
dirPath = "/home/cyberfox/iitm/"
rangeCommand = ""

os.system("clear")
t = time.time()
z = os.listdir(dirPath)
l = len(z)

ap = argparse.ArgumentParser()
ap.add_argument("-x","--diameter",required=True,help="RADAR diameter in KM [ X axis ]")
ap.add_argument("-y","--height",required=True,help="RADAR height in KM [ Y axis ]")
ap.add_argument("-l","--lower",required=False,help="Lower range of Reflectivity")
ap.add_argument("-u","--upper",required=False,help="Upper range of Reflectivity")
args = vars(ap.parse_args())

lowerRange = int(args["lower"])
upperRange = int(args["upper"])

if(lowerRange != None and upperRange != None):
	rangeCommand = " -l " + str(lowerRange) + " -u " + str(upperRange)
else:
	rangeCommand = ""

RADAR_DIAMETER = int(args["diameter"])
RADAR_HEIGHT = int(args["height"])
print "USER INPUT PARAMETERS:\n\nTotal distace on X-axis :%s KMs\nTotal height on Y-axis :%s KMs" % (str(RADAR_DIAMETER),str(RADAR_HEIGHT))
print "Upper reflectivity limit(dB): %s\nLower reflectivity limit(dB): %s" % (str(upperRange),str(lowerRange))

for i in range(0,l):
    s = str(z[i])
    if (s.endswith('.png') or s.endswith('.bmp') or s.endswith('.jpg')): #and (s.startswith('c')):
        cmd = "python cloud.py -i " + s + " -x " + str(RADAR_DIAMETER) + " -y " + str(RADAR_HEIGHT) + rangeCommand
        os.system(cmd)
    else:
        pass

print "\nTime required for script execution: "+str(round(time.time()-t,3))+" Seconds\n"
