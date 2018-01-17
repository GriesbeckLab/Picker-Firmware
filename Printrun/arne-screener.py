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

def snapImages():
    """ This function snaps a picture with a given excitation, emission and exposure time, and returns an image """
    core.setAutoShutter(0)
    core.setExposure(1000)


    picker.emission('485')
    picker.lightOn('royalblue')
    time.sleep(1.0)
    green = snapImage(2000)

    picker.emission('535')
    fret = snapImage(2000)
    picker.lightOff('royalblue')

    picker.lightOn('cyan')
    red = snapImage(1000)
    picker.lightOff('cyan')

    
    images = numpy.hstack([green, fret, red,])
    return images

plate_name = tkSimpleDialog.askstring('File', 'Plate Name:')

picker = robot.picker()
picker.connect()
picker.homefilter()

time.sleep(1) # maybe not necessary?

''' Measurement Codeblock
This section of code allows the user to select the file location, records images and calculated FRET ratios, and prompts the user to spray the plates.
'''
# Gets the directory location for saving the files
#directory = tkFileDialog.askdirectory()
#plate_name = tkSimpleDialog.askstring('File', 'Plate Name:')

# Gets the date in the nice string format, to add to the graphs at the end
#datestr = time.strftime("%d %b %Y %H:%M:%S", time.localtime())




filters = ["485","505","535","570","600","630","712"]
lights = ["royalblue","blue","cyan","green","white","red","red"]

data = numpy.memmap(plate_name, dtype='uint16', mode='w+', shape=(20,1040,4176))

timePeriod = 10.0



init = time.time()
t = time.time() - init
if t <= timePeriod:
    delay = timePeriod-t
    time.sleep(delay)
    print 'here'
    print delay
for i in range(10):
    init2 = time.time()
    data[i,:,:] = snapImages()

    # This code account for the variable delay in recording an imaage.
    t = time.time() - init2 
    if t <= timePeriod:
        delay = timePeriod-t
        time.sleep(delay)
    print "Recording %d of 10" %(i+1)


# Prompts the user to add cAMP, then records 25 data points for each colony, at 15 second intervals.
tkMessageBox.showinfo("Command", "Add Calcium")
print "continuing after Calcium addition"



init = time.time()
t = time.time() - init
if t <= timePeriod:
    delay = timePeriod-t
    time.sleep(delay)
    print 'here'
    print delay
for i in range(10,20):
    init2 = time.time()
    data[i,:,:] = snapImages()

    # This code account for the variable delay in recording an imaage.
    t = time.time() - init2 
    if t <= timePeriod:
        delay = timePeriod-t
        time.sleep(delay)
    print "Recording %d of 20" %(i+1)



data.flush()   
print data
print numpy.shape(data)


print "finished recording images"




