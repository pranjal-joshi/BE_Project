#!/usr/bin/python

# Author: Pranjal Joshi
# Date 	: 26-10-2016

import os
import sys
import argparse
import time
import MySQLdb as mdb
import matplotlib.pyplot as plt
import numpy as np

SHOW_PLOT = False

# Database connection manager
try:
	con = mdb.connect("localhost","root","linux")
	db = con.cursor()
except Exception as e:
	raise e
	sys.exit("Failed to connect MySQL database! Check credentials & make sure that MySQL server is running in background.")

def initDB():
	try:
		print "Initializing database to store analyzed data..."
		db.execute("show databases")
		a = db.fetchall()
		a = str(a)
		if(a.find("cloudTracking") > 0):
			db.execute("drop database cloudTracking")
			con.commit()
		else:
			pass
		# Create new database while starting batch processing each time.
		db.execute("create database cloudTracking")
		db.execute("use cloudTracking")
		db.execute("create table image_table(iid INT AUTO_INCREMENT, datetime VARCHAR(40), PRIMARY KEY(iid))")
		db.execute("create table cloud_table(iid INT, cid INT, area FLOAT)")
		con.commit()
		print "Database created successfully!\n"
	except Exception as e:
		raise e
		sys.exit("Something went wrong, Failed to initialize database correctly!!")

def closeDB():
	print "Closing database..."
	con.close()


def plotGraph():
	print "\nPlotting analyzed data... Please wait...\n"
	db.execute("use cloudTracking")
	db.execute("select datetime from image_table")
	fetchTime = db.fetchall()
	cnt = len(fetchTime)
	timeArray = []
	for i in range(0,cnt):
		if((int(fetchTime[i][0][0]) != 1) and (int(fetchTime[i][0][0]) != 0)):		# check if time starts with 0x.min or 1x.min
			temp = "0" + fetchTime[i][0]
			timeArray.append(temp)
		else:
			temp = fetchTime[i][0]
			timeArray.append(temp)

	timeArray.sort()
	db.execute("select max(iid) from cloud_table")
	maxImages = db.fetchone()
	maxImages = int(maxImages[0])
	db.execute("select max(cid) from cloud_table")
	maxClouds = db.fetchone()
	maxClouds = int(maxClouds[0])
	db.execute("select max(area) from cloud_table")
	maxArea = db.fetchone()
	maxArea = int(maxArea[0])

	fig = plt.figure()

	for cldCnt in range(1,maxClouds+1):
		db.execute("select area from cloud_table where cid=%s" % cldCnt)
		fetchArea = db.fetchall()
		cnt = len(fetchArea)
		areaArray = []
		for k in range(0,cnt):
			areaArray.append(float(fetchArea[k][0]))

		# start plotting
		xAxis = np.arange(0,len(fetchTime))
		areaArray = np.array(areaArray)
		yAxis = areaArray
		yAxis = np.pad(yAxis, pad_width=(len(fetchTime)-len(yAxis)), mode='constant', constant_values=0)[len(fetchTime)-len(yAxis):]	# 0 pad for dimesion match
		xTicks = timeArray
		print "xAxis: ", xAxis
		print "yAxis: ", yAxis
		plt.xticks(xAxis, xTicks)
		plt.ylim((0,maxArea+20))
		plt.xlabel("Time",fontsize=15)
		plt.ylabel("Area (Sq.KM)",fontsize=15)
		plt.title("Cloud Area Statistics",fontsize=30)
		plt.figtext(.5,.86,('For reflectivity range: %s to %s dB.' % (lowerRange, upperRange)),fontsize=10,ha='center')
		plt.grid(True)
		plt.plot(xAxis, yAxis, linewidth=2.0, label=("Cloud " + str(cldCnt)), marker='o')
		plt.legend(loc='upper right', prop={'size':10})
	fig.savefig(dirPath + "/cloudTracking/analyzedPlot.png")
	if SHOW_PLOT:
		plt.show()

# Place input images in this dirctory.
dirPath = "/home/cyberfox/iitm/"
rangeCommand = ""

os.system("clear")
# initialize MySQL database to store analyzed data.
initDB()

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
plotGraph()
closeDB()
