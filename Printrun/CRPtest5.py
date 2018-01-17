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

# Imports the modules for the filterwheel, camera and shutters

sys.path.append("C:\Program Files\Micro-Manager-1.4")
sys.path.append("C:\Users\ng\Desktop\ColonyPicker\Printrun-master")

import MMCorePy
core = MMCorePy.CMMCore();
core.unloadAllDevices(); # makes sure there isn't anything previously loaded


# Loads Camera
core.loadDevice("Camera", "PrincetonInstruments", "Camera-1");


core.initializeAllDevices();
 
filters = ["485","505","535","570","600","630","712"]
lights = ["royalblue","blue","cyan","green","white","red","red"]

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

def snapImages(Exposure):
    """ This function snaps a picture with a given excitation, emission and exposure time, and returns an image """
    core.setAutoShutter(0)
    core.setExposure(Exposure)


    picker.emission(filters[0])
    picker.lightOn(lights[0])
    core.snapImage()
    cyan = core.getImage()

    picker.emission(filters[2])

    core.snapImage()
    fret = core.getImage()
    picker.lightOff(lights[0])

    picker.lightOn(lights[2])
    core.snapImage()
    yellow = core.getImage()
    picker.lightOff(lights[2])

    
    images = numpy.hstack([cyan, fret, yellow,])
    return images



picker = robot.picker()
picker.connect()
illuminationtime = 0.3


picker.homefilter()


time.sleep(1) # maybe not necessary?

raw = snapImages(1000)

data = raw[:,:1392]
img = scipy.misc.toimage(data, high=numpy.max(data), low=numpy.min(data), mode='I')
img.save('cfp.png')

data = raw[:,1392:2724]
img = scipy.misc.toimage(data, high=numpy.max(data), low=numpy.min(data), mode='I')
img.save('fret.png')

data = raw[:,2724:]
img = scipy.misc.toimage(data, high=numpy.max(data), low=numpy.min(data), mode='I')
img.save('yfp.png')

