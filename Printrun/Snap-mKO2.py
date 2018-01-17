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

# imports GUI modules
import tkMessageBox
import tkFileDialog
import tkSimpleDialog
import Tkinter as tk

# hides ugly empty TK window
root = tk.Tk()
root.withdraw()

filters = ["485","505","535","570","600","630","712"]
lights = ["royalblue","blue","cyan","green","white","red","red"]


# Gets the directory location for saving the files
plate_name = tkSimpleDialog.askstring('File', 'Plate Name:')


sys.path.append("C:\Program Files\Micro-Manager-1.4")
sys.path.append("C:\Users\ng\Desktop\ColonyPicker\Printrun-master")


exposure = 1000

# Imports the modules for the filterwheel, camera and shutters
import MMCorePy
core = MMCorePy.CMMCore();
core.unloadAllDevices(); # makes sure there isn't anything previously loaded
# Loads Camera
core.loadDevice("Camera", "PrincetonInstruments", "Camera-1");
core.initializeAllDevices();
# Final setup for camera
core.setCameraDevice("Camera");

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
#picker.home()
#picker.park()

picker.homefilter()


picker.emission(filters[4])
picker.lightOn(lights[3])
image1 = snapImage(3000)
picker.lightOff(lights[3])

picker.emission(filters[4])
picker.lightOn(lights[3])
image2 = snapImage(2000)
picker.lightOff(lights[3])

picker.emission(filters[4])
picker.lightOn(lights[3])
image3 = snapImage(1000)
picker.lightOff(lights[3])

numpy.save('mKO2_3000_' + plate_name ,image1)
img = scipy.misc.toimage(image1, high=numpy.max(image1), low=numpy.min(image1), mode='I')
img.save('mKO2_3000' + plate_name + '.png')

numpy.save('mKO2_2000_' + plate_name,image2)
img = scipy.misc.toimage(image2, high=numpy.max(image2), low=numpy.min(image2), mode='I')
img.save('mKO2_2000' + plate_name +'.png')

numpy.save('mKO2_1000_' + plate_name,image3)
img = scipy.misc.toimage(image3, high=numpy.max(image3), low=numpy.min(image3), mode='I')
img.save('mKO2_1000' + plate_name +'.png')



