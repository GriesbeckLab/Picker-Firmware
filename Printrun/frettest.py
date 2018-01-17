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
t = time.time()
sleeptime = 1
illuminationtime = 0.3


picker.homefilter()
print "fininished homing filter" + str(time.time() - t)

time.sleep(1) # maybe not necessary?
print "fininished first sleep" + str(time.time() - t)
t1 = time.time()



''' Measurement Codeblock
This section of code allows the user to select the file location, records images and calculated FRET ratios, and prompts the user to spray the plates.
'''
# Gets the directory location for saving the files
directory = tkFileDialog.askdirectory()
plate_name = tkSimpleDialog.askstring('File', 'Plate Name:')

# Gets the date in the nice string format, to add to the graphs at the end
datestr = time.strftime("%d %b %Y %H:%M:%S", time.localtime())

# Checks to see if the plate name is actually there, exit if nothing has been entered in the popup box
if len(plate_name) == 0:
    sys.exit()
if not directory:
    sys.exit()



filters = ["485","505","535","570","600","630","712"]
lights = ["royalblue","blue","cyan","green","white","red","red"]


for i in range(0,1):

    picker.emission(filters[0])
    print "fininished filter change to" + str(filters[i])+ " " + str(time.time() - t1)
    picker.lightOn(lights[0])
    t1 = time.time()
    a = snapImage(100)  
    img = scipy.misc.toimage(a, high=numpy.max(a), low=numpy.min(a), mode='I')
    img.save("20141024AF_"+ str(i) + "_Donor_"   + str(time.time()) +'.png')
    picker.lightOff(lights[0])
    time.sleep(sleeptime)
    picker.emission(filters[2])
    print "fininished filter change to" + str(filters[i])+ " " + str(time.time() - t1)
    picker.lightOn(lights[0])
    t1 = time.time()
    b = snapImage(100)  
    img = scipy.misc.toimage(b, high=numpy.max(b), low=numpy.min(b), mode='I')
    img.save("20141024AF_" + str(i) + "_FRET_"   + str(time.time()) +'.png')
    picker.lightOff(lights[0])      

   


print "finished recording images"


#picker.lightOn('white')
#time.sleep(1)
#picker.lightOff('white')



