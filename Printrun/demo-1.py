import transformation
import numpy
import math
import analyzer
import robot
import scipy.ndimage
import skimage.measure
import PIL
import time
import sys
import scipy.misc
import pylab as pl
import time

import tkMessageBox
import tkFileDialog
import tkSimpleDialog
import Tkinter as tk


# hides ugly empty TK window
root = tk.Tk()
root.withdraw()

sys.path.append("C:\Program Files\Micro-Manager-1.4")
sys.path.append("C:\Users\ng\Desktop\ColonyPicker\Printrun-master")


exposure = 1000


picker = robot.picker()
picker.connect()

picker.home()

center = [-50,28]
points = []
for x in range(-40,50,20):
    for y in range(-40,50,20):
        if math.sqrt(x**2 + y**2) <= 40:
        	points.append([x,y])
print points
print len(points)   

picker.moveToSafeHeight()

picker.park()

tkMessageBox.showinfo("Command", "Turn off lights")

illuminationtime = 0.3
picker.lightOn('white')
time.sleep(2)
picker.lightOff('white')

picker.lightOn('royalblue')
time.sleep(2)
picker.lightOff('royalblue')

picker.lightOn('blue')
time.sleep(2)
picker.lightOff('blue')

picker.lightOn('cyan')
time.sleep(2)
picker.lightOff('cyan')

picker.lightOn('green')
time.sleep(2)
picker.lightOff('green')

picker.lightOn('amber')
time.sleep(2)
picker.lightOff('amber')

picker.lightOn('red')
time.sleep(2)
picker.lightOff('red')

tkMessageBox.showinfo("Command", "Add plate")
picker.lightOn('blue')
tkMessageBox.showinfo("Command", "Continue?")
picker.lightOff('blue')

tkMessageBox.showinfo("Command", "Turn on lights")

time.sleep(1) # maybe not necessary?

picker.moveToSafeHeight()

for point in points:


    picker.move(point[0]+center[0], point[1]+center[1], 20.0)

    picker.move(point[0]+center[0], point[1]+center[1], 10.0)

    time.sleep(0.2)
    picker.move(point[0]+center[0], point[1]+center[1], 20.0) 

picker.home()
