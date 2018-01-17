# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# imports vital stuff for imgae processing, getting the time and date, etc...
import PIL
import time
import sys
import scipy.misc
import numpy
import pylab as pl
import matplotlib.cm as cm 
sys.path.append("C:\Program Files\Micro-Manager-1.4")
sys.path.append("C:\Users\ng\Desktop\ColonyPicker\Printrun-master")
import robot

import tkMessageBox
import tkFileDialog
import tkSimpleDialog
import Tkinter as tk
# hides ugly empty TK window
root = tk.Tk()
root.withdraw()

plate_name = tkSimpleDialog.askstring('File', 'Plate Name:')

# Imports the modules for the filterwheel, camera and shutters
import MMCorePy
core = MMCorePy.CMMCore();
core.unloadAllDevices(); # makes sure there isn't anything previously loaded


# Loads Camera
core.loadDevice("Camera", "PrincetonInstruments", "Camera-1");


core.initializeAllDevices();
 


# Final setup for camera
core.setCameraDevice("Camera");

# <codecell>
# The functions used in the program!
def snapImage(Exposure):
    """ This function snaps a picture with a given excitation, emission and exposure time, and returns an image """
    core.setAutoShutter(0)
    core.setExposure(Exposure)
    core.setShutterOpen(1)
    core.snapImage()
    pic = core.getImage()
    core.setShutterOpen(0)
    return pic


# <codecell>
p = robot.picker()
p.connect()

#p.home()
#p.moveToSafeHeight()
#p.park()
while p.connection.printing:
    time.sleep(0.1)
    
p.lightOn('royalblue')
a = snapImage(600)
p.lightOff('royalblue')


time.sleep(1)

p.lightOn('cyan')
b = snapImage(600)
p.lightOff('cyan')



img = scipy.misc.toimage(a, high=numpy.max(a), low=numpy.min(a), mode='I')
img.save(plate_name + '-donor.png')


img = scipy.misc.toimage(b, high=numpy.max(b), low=numpy.min(b), mode='I')
img.save(plate_name + '-acceptor.png')


'''
img = scipy.misc.toimage(a, mode='I')
img.save(plate_name + '-a.png')

img = scipy.misc.toimage(b, mode='I')
img.save(plate_name + '-b.png')


numpy.save(plate_name + '-a', a)
numpy.save(plate_name + '-b', b)

'''
sys.exit()
#init_picture = snapImage(donorEx,donorEm,exposure)
# these are the parameters for the mask, such as height and width, and diameter of the circle.




