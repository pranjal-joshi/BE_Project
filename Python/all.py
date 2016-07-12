#!/usr/bin/python

import os

dirPath = "/root/iitm/"
z = os.listdir(dirPath)
l = len(z)
for i in range(0,l):
    s = str(z[i])
    if s.endswith('.png') or s.endswith('.bmp') or s.endswith('.jpg'):
        cmd = "python demo.py -i " + s
        os.system(cmd)
    else:
        pass
