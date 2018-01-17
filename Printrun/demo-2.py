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
import matplotlib.pyplot as plt

from skimage.feature import match_template
import scipy.ndimage
import skimage.feature


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


    picker.emission(filters[2])
    picker.lightOn(lights[1])
    time.sleep(1.0)
    green = snapImage(500)
    picker.lightOff(lights[1])
    return green


picker = robot.picker()
picker.connect()
picker.home()
picker.moveToSafeHeight()
picker.park()
picker.homefilter()

tkMessageBox.showinfo("Command", "Add plate and close door")

time.sleep(1)

''' Measurement Codeblock
This section of code allows the user to select the file location, records images and calculated FRET ratios, and prompts the user to spray the plates.
'''





filters = ["485","505","535","570","600","630","712"]
lights = ["royalblue","blue","cyan","green","white","red","red"]


timePeriod = 5.0

img = snapImages()

def twoD_Gaussian((x, y), amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    xo = float(xo)
    yo = float(yo)    
    a = (numpy.cos(theta)**2)/(2*sigma_x**2) + (numpy.sin(theta)**2)/(2*sigma_y**2)
    b = -(numpy.sin(2*theta))/(4*sigma_x**2) + (numpy.sin(2*theta))/(4*sigma_y**2)
    c = (numpy.sin(theta)**2)/(2*sigma_x**2) + (numpy.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*numpy.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) 
                            + c*((y-yo)**2)))
    return g.ravel()

x = numpy.linspace(0, 16, 17)
y = numpy.linspace(0, 16, 17)
x, y = numpy.meshgrid(x, y)

#create data
template = twoD_Gaussian((x, y), 300, 8, 8, 3, 3, 2, 10).reshape(17,17)
result = skimage.feature.match_template(img, template)

im = numpy.where(result > 0.7, 1, 0)
label, numberOfColonies = scipy.ndimage.label(im)
colonyLocations = scipy.ndimage.measurements.center_of_mass(im, label, numpy.arange(1,numberOfColonies))

AreaMask = numpy.zeros([1040,1392])
for i in colonyLocations:
    AreaMask[int(i[0]+8), int(i[1])+8] = 1
AreaMask = scipy.ndimage.binary_dilation(AreaMask, iterations=4)
colonyAreaMask, numberOfColonies = scipy.ndimage.label(AreaMask)

plt.figure(0, (6,10))
plt.subplot(2,1,1)
plt.imshow(img, cmap = 'gray')
plt.title("Fluorescent Image")
plt.axis("off")
plt.subplot(2,1,2)
plt.imshow(colonyAreaMask)
plt.title(str(numberOfColonies) + " Colonies Detected")
#plt.annotate("Colonies found: %d" %(numberOfColonies[1]-1), xy = (50,50),bbox = dict(boxstyle = 'round,pad=0.2', fc = 'yellow'))
plt.axis("off")
plt.show()
imageOK = tkMessageBox.askyesno('Option',' Open door and Continue?') # Dialog box: Do you want to continue?
print "here"
print imageOK
if not(imageOK):
    sys.exit()





init = time.time()
t = time.time() - init
if t <= timePeriod:
    delay = timePeriod-t
    time.sleep(delay)
    print 'here'
    print delay
for i in range(3):
    init2 = time.time()
    data = snapImages()

    # This code account for the variable delay in recording an imaage.
    t = time.time() - init2 
    if t <= timePeriod:
        delay = timePeriod-t
        time.sleep(delay)
    print "Recorded %d of 3" %(i+1)


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
for i in range(3,6):
    init2 = time.time()
    data = snapImages()

    # This code account for the variable delay in recording an imaage.
    t = time.time() - init2 
    if t <= timePeriod:
        delay = timePeriod-t
        time.sleep(delay)
    print "Recorded %d of 6" %(i+1)

print "finished recording images"

imageOK = tkMessageBox.askyesno('Option',' Pick Colonies?') # Dialog box: Do you want to continue?


center = [-50,28]
points = [[-60,20], [-40,30],[-50,50]]



for point in points:
    picker.pickNextBead()    
    picker.pickColony(point)
    picker.innoculateNextWell()
    
    picker.home()


