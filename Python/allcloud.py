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
import multiprocessing
import math
import progressbar

# Global varables
THREADS = 4
SEQUENTIAL = False
SHOW_PLOT = False
dirPath = os.path.abspath('.')		#"/home/cyberfox/iitm/"
if(not(os.path.isdir(os.path.join(dirPath,'cloudTracking')))):
	os.system("mkdir cloudTracking")
rangeCommand = ""
XDIVS = 10
SMOOTHENER = 1
p = None
c = None
cmds = []
z_new = []
BLOCK_CHAR = u"\u2588"

# for printing colorful text
class colorText:
	HEAD = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	WARN = '\033[93m'
	FAIL = '\033[91m'
	END = '\033[0m'
	BOLD = '\033[1m'
	UNDR = '\033[4m'

os.system("clear")

# Database connection manager
try:
	print colorText.GREEN + "Initializing database to store analyzed data..." + colorText.END
	con = mdb.connect("localhost","root","linux")
	db = con.cursor()
except Exception as e:
	try:
		con = mdb.connect("localhost","root","winx1234")
		db = con.cursor()
		db.execute("use cloudTracking")
	except Exception as e:
		raise e
		sys.exit(colorText.FAIL + "Failed to connect MySQL database! Check credentials & make sure that MySQL server is running in background." + colorText.END)

def initDB():
	try:
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
		print colorText.GREEN + "Database created successfully!\n" + colorText.END
	except Exception as e:
		raise e
		sys.exit(colorText.FAIL + "Something went wrong, Failed to initialize database correctly!!" + colorText.END)

def closeDB():
	print colorText.WARN + "\nClosing database...\n" + colorText.END
	con.close()

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def plotGraph():
	print colorText.BOLD + colorText.UNDR + colorText.HEAD + "\nPlotting analyzed data... Please wait...\n" + colorText.END
	db.execute("use cloudTracking")
	db.execute("select datetime from image_table")
	fetchTime = db.fetchall()
	cnt = len(fetchTime)
	timeArray = []
	correctionCount = 0
	for i in range(0,cnt):
		if((i%(round(cnt/XDIVS)+1) == 0) or (i == cnt-1)):
			if((int(fetchTime[i][0][0]) != 1) and (int(fetchTime[i][0][0]) != 0)):		# check if time starts with 0x.min or 1x.min
				temp = "0" + fetchTime[i][0]
				timeArray.append(temp)
			else:
				temp = fetchTime[i][0]
				timeArray.append(temp)
			correctionCount += 1
		else:
			pass
	db.execute("select max(iid) from cloud_table")
	maxImages = db.fetchone()
	maxImages = int(maxImages[0])
	db.execute("select max(cid) from cloud_table")
	maxClouds = db.fetchone()
	maxClouds = int(maxClouds[0])
	db.execute("select max(area) from cloud_table")
	maxArea = db.fetchone()
	maxArea = int(maxArea[0])

	fig = plt.figure(figsize=(16,9))

	for cldCnt in range(1,maxClouds+1):
		db.execute("select area from cloud_table where cid=%s" % cldCnt)
		fetchArea = db.fetchall()
		cnt = len(fetchArea)
		areaArray = np.zeros((maxImages),np.float16)
		for k in range(0,cnt):
			#db.execute("select iid from cloud_table where cast(area as decimal)=cast(%s as decimal)" % str(fetchArea[k][0]))
			db.execute("select iid from cloud_table where abs(area - %s) < 0.0005" % str(fetchArea[k][0]))
			index = db.fetchone()
			index = int(index[0])
			areaArray[index-1] = float(fetchArea[k][0])

		# start plotting
		xAxis = np.arange(0,len(fetchTime))
		areaArray = np.array(areaArray)
		yAxis = areaArray
		yAxis = np.pad(yAxis, pad_width=(len(fetchTime)-len(yAxis)), mode='constant', constant_values=0)[len(fetchTime)-len(yAxis):]	# 0 pad for dimesion match
		xTicks = timeArray
		#print "xAxis: ", xAxis
		#print "yAxis: ", yAxis
		plt.xticks(xAxis, xTicks)
		plt.ylim((0,maxArea+20))
		plt.xlabel("Time",fontsize=15)
		plt.ylabel("Area (Sq.KM)",fontsize=15)
		plt.title("Cloud Area Statistics",fontsize=30)
		plt.figtext(.5,.86,('For reflectivity range: %s to %s dB.' % (lowerRange, upperRange)),fontsize=10,ha='center')
		plt.grid(True)
		plt.locator_params(axis='x', nbins=XDIVS)		# limits x-labels to 10. Eliminates crowd on X axis.
		plt.plot(xAxis, smooth(yAxis,SMOOTHENER), linewidth=1.5, label=("Cloud " + str(cldCnt)),marker='o') #marker='o'
		plt.legend(loc='upper right', prop={'size':10})
		#plt.plot(xAxis, yAxis, linewidth=1,ls='dotted',label='_nolegend_')
	fig.savefig(dirPath + "/cloudTracking/analyzedPlot.png")
	if SHOW_PLOT:
		plt.show()

def ex(d):
	os.system(d)

def rangeMap(x,inmin,inmax,outmin,outmax,roundoff=False):
	z = (x-inmin)*(outmax-outmin)/(inmax-inmin)+outmin;
	if not roundoff:
		return z
	else:
		return round(z)

def runThread():
	global c
	tmp = 0
	bar = progressbar.ProgressBar(maxval=int(math.ceil(len(z_new)/THREADS)+2),widgets=[progressbar.Bar(BLOCK_CHAR,'[',']'),' ',progressbar.Percentage()])
	print "Processing...\n"
	bar.start()
	for c in range(1,int(math.ceil(len(z_new)/THREADS)+2)):
		global p
		jobs = []
		for i in range(THREADS):
			try:
				p = multiprocessing.Process(target=ex,args=(cmds[tmp+i],))
				jobs.append(p)
				p.start()
				bar.update(c)#rangeMap((c*i+1),1,len(cmd),1,100,roundoff=True))
				time.sleep(0.25)
			except:
				print "All threads have been started."
				break
		try:
			p.join()
		except:
			pass
		p = None
		tmp += THREADS
	bar.finish()

# initialize MySQL database to store analyzed data.
initDB()

t = time.time()
z = sorted(os.listdir(dirPath))			# Read files in sequential manner.
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
print colorText.WARN + colorText.BOLD + "USER INPUT PARAMETERS:\n\nTotal distace on X-axis :%s KMs\nTotal height on Y-axis :%s KMs" % (str(RADAR_DIAMETER),str(RADAR_HEIGHT))
print "Upper reflectivity limit(dB): %s\nLower reflectivity limit(dB): %s\n" % (str(upperRange),str(lowerRange)) + colorText.END

print colorText.BLUE + colorText.BOLD + "SYSTEM INFORMATION:\n\nAvailabe CPU Cores: %d" % (multiprocessing.cpu_count())
print "No. of parallel threads: %s\n" % (str(THREADS) if (SEQUENTIAL == False) else "1 [SEQUENTIAL flag is activated manually]") + colorText.END

if SEQUENTIAL:
	for i in range(0,l):
		s = str(z[i])
		if(s.find('KASPR') > -1):
			z_new.append(s)

	l = len(z_new)
	z = z_new
	bar = progressbar.ProgressBar(maxval=l,widgets=[progressbar.Bar(BLOCK_CHAR,'[',']'),' ',progressbar.Percentage()])
	print "Processing...\n"
	bar.start()
	for i in range(0,l):
	    s = str(z[i])
	    if (s.find('KASPR') > -1):
	        cmd = "python cloud.py -i " + s + " -x " + str(RADAR_DIAMETER) + " -y " + str(RADAR_HEIGHT) + rangeCommand
		bar.update(i)
	        os.system(cmd)
	    else:
	        pass
	bar.finish()
else:
	# Pre-process paths for parallel execution
	for i in range(0,l):
		temp = z[i]
		if(temp.find('KASPR') == -1):
			pass
		else:
			z_new.append(temp)

	for i in range(0,len(z_new)):
		cmd = "python ./cloud.py -i " + z_new[i] + " -x " + str(RADAR_DIAMETER) + " -y " + str(RADAR_HEIGHT) + rangeCommand
		cmds.append(cmd)

	# Multithreading begins...
	runThread()

plotGraph()
print colorText.GREEN + "\nTime required for script execution: "+str(round(time.time()-t,3))+" Seconds\n" + colorText.END
closeDB()
