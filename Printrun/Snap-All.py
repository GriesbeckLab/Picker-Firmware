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


filters = ["485","505","535","570","600","630","712"]
lights = ["royalblue","blue","cyan","green","white","red","red"]


sys.path.append("C:\Program Files\Micro-Manager-1.4")
sys.path.append("C:\Users\ng\Desktop\ColonyPicker\Printrun-master")


exposure = 300

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
picker.lightOn(lights[0])
for wavelength in filters:
    
    picker.emission(wavelength)
    image = snapImage(3000)
    img = scipy.misc.toimage(image, high=numpy.max(image), low=numpy.min(image), mode='I')
    img.save(wavelength + '.png')
picker.lightOff(lights[0])
#picker.homefilter()
picker.emission(2)


