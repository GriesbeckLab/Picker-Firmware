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

import tkMessageBox
import tkFileDialog
import tkSimpleDialog
import Tkinter as tk
# hides ugly empty TK window
root = tk.Tk()
root.withdraw()

plate_name = tkSimpleDialog.askstring('File', 'Plate Name:')

sys.path.append("C:\Program Files\Micro-Manager-1.4")
sys.path.append("C:\Users\ng\Desktop\ColonyPicker\Printrun-master")

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


picker = robot.picker()
picker.connect()
picker.homefilter()
picker.home()

picker.park()
time.sleep(3)


picker.lightOn('royalblue')
picker.emission('485')

time.sleep(5)

a = snapImage(300)

picker.emission('535')

time.sleep(5)

b = snapImage(300)

picker.lightOff('royalblue')
time.sleep(3)

picker.lightOn('cyan')
c = snapImage(300)

picker.lightOff('cyan')

print "finished recording images"

img = scipy.misc.toimage(a, high=numpy.max(a), low=numpy.min(a), mode='I')
img.save(plate_name + '-donor.png')


img = scipy.misc.toimage(b, high=numpy.max(b), low=numpy.min(b), mode='I')
img.save(plate_name + '-FRET.png')
   
img = scipy.misc.toimage(b, high=numpy.max(c), low=numpy.min(c), mode='I')
img.save(plate_name + '-acceptor.png')


#picker.lightOn('white')
#time.sleep(1)
#picker.lightOff('white')



