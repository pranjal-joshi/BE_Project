#!/usr/bin/python
import math, sys
import time
import pp
import os

ppservers = ("*",)

js = pp.Server(ppservers=ppservers,socket_timeout=720000)
js.set_ncpus(0)
print "CPUs: " + str(js.get_ncpus())
print str(js.get_active_nodes())

def chk(a):
	while a<100:
		a=a+1
		time.sleep(0.01)
	print a
	a=0

f = js.submit(chk,(0,),(),("time","os"))
print str(js.get_active_nodes())
js.print_stats()
r = f()
js.print_stats()
