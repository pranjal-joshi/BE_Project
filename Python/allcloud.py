#!/usr/bin/python

# Author: Pranjal Joshi
# Date 	: 26-10-2016

import os
import sys
import argparse
import time

os.system("clear")
t = time.time()
dirPath = "/root/iitm/"
z = os.listdir(dirPath)
l = len(z)

ap = argparse.ArgumentParser()
ap.add_argument("-x","--diameter/radius",required=True,help="RADAR diameter in KM [ X axis ]")
ap.add_argument("-y","--height",required=True,help="RADAR height in KM [ Y axis ]")
args = vars(ap.parse_args())

RADAR_RADIUS = int(args["diameter/radius"])
RADAR_HEIGHT = int(args["height"])
print "USER INPUT PARAMETERS:\n\nTotal distace on X-axis :%s KMs\nTotal height on Y-axis :%s KMs" % (str(RADAR_RADIUS),str(RADAR_HEIGHT))

for i in range(0,l):
    s = str(z[i])
    if (s.endswith('.png') or s.endswith('.bmp') or s.endswith('.jpg')) and (s.startswith('c')):
        cmd = "python cloud.py -i " + s + " -x " + str(RADAR_RADIUS) + " -y " + str(RADAR_HEIGHT)
        os.system(cmd)
    else:
        pass

print "\nTime required for script execution: "+str(round(time.time()-t,3))+" Seconds\n"