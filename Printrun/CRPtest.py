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
    yellow = core.getImage()
    picker.lightOff(lights[0])
    images = numpy.hstack([cyan, yellow,])
    return images



picker = robot.picker()
picker.connect()
illuminationtime = 0.3

picker.home()
picker.park()
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

data = snapImages(500)

img = scipy.misc.toimage(data, high=numpy.max(data), low=numpy.min(data), mode='I')
img.save('t.png')

data = snapImages(500)[numpy.newaxis,...]

init = time.time()
t = time.time() - init
if t <= 5:
    delay = 5-t
    time.sleep(delay)
    print 'here'
    print delay
for i in range(1):
    init2 = time.time()
    data = numpy.vstack([data, snapImages(500)[numpy.newaxis,...]])

    # This code account for the variable delay in recording an imaage.
    t = time.time() - init2 
    if t <= 5.0:
        delay = 5.0-t
        time.sleep(delay)
    print "Recording %d of 10" %(i+1)



# Prompts the user to add Isopropanol, then records 25 data points for each colony, at 15 second intervals.
tkMessageBox.showinfo("Command", "Add Isopropanol")
print "continuing after Isopropanol addition"


init = time.time()
t = time.time() - init
if t <= 5:
    delay = 5-t
    time.sleep(delay)
    print 'here'
    print delay
for i in range(1):
    init2 = time.time()
    data = numpy.vstack([data, snapImages(500)[numpy.newaxis,...]])

    # This code account for the variable delay in recording an imaage.
    t = time.time() - init2 
    if t <= 5.0:
        delay = 5.0-t
        time.sleep(delay)
    print "Recording %d of 10" %(i+1)


# Prompts the user to add cAMP, then records 25 data points for each colony, at 15 second intervals.
tkMessageBox.showinfo("Command", "Add cAMP")
print "continuing after cAMP addition"



init = time.time()
t = time.time() - init
if t <= 5:
    delay = 5-t
    time.sleep(delay)
    print 'here'
    print delay
for i in range(1):
    init2 = time.time()
    data = numpy.vstack([data, snapImages(500)[numpy.newaxis,...]])

    # This code account for the variable delay in recording an imaage.
    t = time.time() - init2 
    if t <= 5.0:
        delay = 5.0-t
        time.sleep(delay)
    print "Recording %d of 30" %(i+1)



    


   
print data
print numpy.shape(data)
numpy.save("data", data)

print "finished recording images"




