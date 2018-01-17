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
import matplotlib.pyplot as plt
import transformation


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


filters = ["485","505","535","570","600","630","712"]
lights = ["royalblue","blue","cyan","green","white","red","red"]
delaytime = 3.0

# <codecell>
# The functions used in the program!
def snapImage(Exposure):
    """ This function snaps a picture with a given excitation, emission and exposure time, and returns an image """
    core.setAutoShutter(0)
    core.setExposure(Exposure)
    picker.emission(filters[2])
    picker.lightOn(lights[2])
    core.snapImage()
    pic = core.getImage()
    picker.lightOff(lights[2])
    core.setShutterOpen(0)
    return pic

def snapImages(Exposure):
    """ This function snaps a picture with a given excitation, emission and exposure time, and returns an image """
    core.setAutoShutter(0)
    core.setExposure(Exposure)


    picker.emission(filters[2])
    picker.lightOn(lights[2])
    core.snapImage()
    green = core.getImage()

    picker.emission(filters[3])

    core.snapImage()
    fret = core.getImage()
    picker.lightOff(lights[2])

    picker.lightOn(lights[3])
    core.snapImage()
    red = core.getImage()
    picker.lightOff(lights[3])

    
    images = numpy.hstack([green, fret, red,])
    return images

def newMask():
    """ This function generates a mask, that sets the area outside the plate to black. Its an array of zeros the size of the picture, with a filled circle of 1's in the location of the petri dish. This is done to make the colony-detection algorithm work more accurately.
    """
    # these are the parameters for the mask, i.e. its height and width, and radius and center of the circle as measured in pixels. The circle parameters are determined by measuring a picture taken of a plate.
    h,w = 1040, 1392
    a,b = 480, 720
    r = 400
    y,x = numpy.ogrid[-a:h-a, -b:w-b]
	# Thanks, Mr. Pythagorus!
    mask = x*x + y*y <= r*r
    array = numpy.zeros((h, w))
    array[mask] = 1
    return array

def segmentImage(picture):
    """ This function takes a picture, and tries to isolate the colonies
    """
	# creates a new mask, from the function above
    mask = newMask()
	#uses the mask to get rid of the background
    masked = mask*picture
	# only takes pixels 3 times greater than the standard deviation of the pixel intensity. This has been found to reliably find only fluorecent colonies in our system.
    binaryImage = numpy.where(masked>numpy.mean(picture)+2*numpy.std(picture),1,0)
	# This function eroded the binary image, getting rid of tiny specs, and removing the edges of blobs.
    binaryImage = scipy.ndimage.binary_erosion(binaryImage)
	# This function fill in any gaps in blobs.
    binaryImage = scipy.ndimage.binary_opening(binaryImage,structure=numpy.ones((2,2)))
	# This function identifies the colonies, and gives them labels and a total.
    labeled,nr_objects = scipy.ndimage.label(binaryImage)
    return labeled,nr_objects

def getRatiometric(colonies, exposure):
    """ This is takes the location of previously found colonies, and the takes two images, one of the donor and one of FRET.
    It then uses the generated images to get the ratiometric responce for all the colony, using the colony locations.
	It returns an array, of Donor fluorence, FRET fluorescence, and FRET Ratios.  
    """

    core.setAutoShutter(0)
    core.setExposure(exposure)


    picker.emission(filters[2])
    picker.lightOn(lights[2])
    core.snapImage()
    donorIMG = core.getImage()

    picker.emission(filters[3])

    core.snapImage()
    fretIMG = core.getImage()
    picker.lightOff(lights[2])



    
	# Calculates Donor,Acceptor and FRET values
    donorValues = scipy.ndimage.mean(donorIMG, colonies[0], numpy.unique(colonies[0]))
    fretValues = scipy.ndimage.mean(fretIMG, colonies[0], numpy.unique(colonies[0]))
    ratioValues = fretValues/donorValues
	# puts the values together in a 2D array
    data_slice = numpy.vstack([donorValues, fretValues, ratioValues])
    return data_slice

picker = robot.picker()
picker.connect()

picker.home()
picker.moveToSafeHeight()
picker.park()

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


#picker.homefilter()


time.sleep(1) # maybe not necessary?

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

# takes a picture, finds the colonies
picture = snapImage(1000)
colonies = segmentImage(picture)

# generates plots for the user to decide if they want to continue, e.g. have the correct filters and exposure time been chosen to generate good images? Have enough colonies been found? If not, exit gracefully.
plt.figure(0, (6,10))
plt.subplot(2,1,1)
plt.imshow(picture[:,:]*100, cmap = 'gray')
plt.axis("off")
plt.subplot(2,1,2)
plt.imshow(colonies[0][:,:], cmap = 'jet')
plt.annotate("Colonies found: %d" %int(colonies[1]-1), xy = (50,50),bbox = dict(boxstyle = 'round,pad=0.2', fc = 'yellow'))
plt.axis("off")
plt.show()
imageOK = tkMessageBox.askyesno('Option','Continue?') # Dialog box: Do you want to continue?
print "here"
print imageOK
if not(imageOK):
    sys.exit()

# The user is satisfied, so go on to record the baseline ratiometric values and plot them in realtime. It records 5 data points for each colony, at 15 second intervals
plt.close()
core.setShutterOpen(1)
core.setAutoShutter(0)
init = time.time()
data = getRatiometric(colonies, 100)[numpy.newaxis,...]
t = time.time() - init
fig = plt.figure(1)
plt.plot(data[:,2,:])
plt.title('Colony Traces from Plate: ' + plate_name + ', at ' + datestr)
fig.canvas.draw()
plt.show(block=False)
# Turns on real-time plotting in Matplotlib
 



if t <= delaytime:
    delay = delaytime-t
    time.sleep(delay)
    print 'here'
    print delay
for i in range(5):
    init2 = time.time()
    data = numpy.vstack([data, getRatiometric(colonies, 100)[numpy.newaxis,...]])
    plt.clf()
    plt.plot(data[:,2,:])
    plt.title('Colony Traces from Plate: ' + plate_name + ', at ' + datestr)
    fig.canvas.draw()
    # This code account for the variable delay in recording an imaage.
    t = time.time() - init2 
    if t <= delaytime:
        delay = delaytime-t
        time.sleep(delay)
    print "Recording %d of 5" %(i+1)


# Prompts the user to add Ionomycin, then records 25 data points for each colony, at 15 second intervals.
tkMessageBox.showinfo("Command", "Add Permeabilization Solution")
print "continuing after ionomycin addition"


init = time.time()
t = time.time() - init
for i in range(5):
    init2 = time.time()
    data = numpy.vstack([data, getRatiometric(colonies, 100)[numpy.newaxis,...]])
    plt.clf()
    plt.plot(data[:,2,:])
    plt.title('Colony Traces from Plate: ' + plate_name + ', at ' + datestr)
    fig.canvas.draw() 
    # This code account for the variable delay in recording an imaage.
    t = time.time() - init2
    if t <= delaytime:
        delay = delaytime-t
        time.sleep(delay)
    print "Recording %d of 5" %(i+1)


# Prompts the user to add Calcium, then records 25 data points for each colony, at 15 second intervals.
tkMessageBox.showinfo("Command", "Add Analyte")
print "continuing after calcium addition"


init = time.time()
t = time.time() - init
for i in range(5):
    init2 = time.time()
    data = numpy.vstack([data, getRatiometric(colonies, 100)[numpy.newaxis,...]])
    plt.clf()
    plt.plot(data[:,2,:])
    plt.title('Colony Traces from Plate: ' + plate_name + ', at ' + datestr)
    fig.canvas.draw()
    # This code account for the variable delay in recording an imaage.
    t = time.time() - init2
    if t <= delaytime:
        delay = delaytime-t
        time.sleep(delay)
    print "Recording %d of 5" %(i+1)
print "Finished aquisition"
# last image update



plt.show(block=True)


''' Analysis Codeblock
This section of code analyses the recorded data, and selects the best responding colonies. It generates plots, highlighting the best responders, and generates an image the shows the best responding colonies locations, to make picking easier.
'''
# Find staring and ending FRET ratios, from 10 reading just before calcium addition, to the last 10 readings. 
start = numpy.mean(data[:3,2,:], axis = 0)
end = numpy.mean(data[-3:,2,:], axis = 0)

# Sort the selection to find those colonies with the greatest response, as defined by change-in-FRET-ratio divided by the starting FRET ratio raised to an arbitrary power. Raised to 1, the starting ratio is ignored, and at 2, has equal value to the ratio change.
selection = (end-start)/(start ** 1.5)
sel = numpy.argsort(selection)



# Scatter plot of Calcium response, with the best ten colonies marked in red
plt.figure(figsize=(9, 6))
plt.scatter(start[sel[-10:]], (end[sel[-10:]]-start[sel[-10:]])/start[sel[-10:]], c = 'r')
plt.scatter(start[sel[0:-10]], (end[sel[0:-10]]-start[sel[0:-10]])/start[sel[0:-10]], c = 'b')
plt.title('Colony Selection from Plate: ' + plate_name + ', at ' + datestr)
plt.xlabel(r'$\o Ca^{2+}\frac{Acceptor}{Donor}$')
plt.ylabel(r'$\frac{(\o Ca^{2+}\frac{Acceptor}{Donor})-(+Ca^{2+}\frac{Acceptor}{Donor})}{\o Ca^{2+}\frac{Acceptor}{Donor}}$')
for i in range(10):
    plt.annotate(i+1, xy = (start[sel[-1-i]],(end[sel[-1-i]]-start[sel[-1-i]])/start[sel[-1-i]]), xytext = (-10, 10),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.2', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
plt.show()

# Traces of Calcium response for the best ten colonies
plt.figure()
plt.plot(numpy.array([numpy.arange(0,numpy.shape(data)[0],1),]*7).T,data[:,2,sel[-1:-8:-1]] );
plt.plot(numpy.array([numpy.arange(0,numpy.shape(data)[0],1),]*3).T,data[:,2,sel[-8:-11:-1]], linestyle='--' );
plt.legend( ('1', '2', '3', '4', '5','6','7','8','9','10'))
plt.title('Colony Traces from Plate: ' + plate_name + ', at ' + datestr)
plt.xlabel(r'Time (second)')
plt.ylabel(r'$\frac{YFP}{Donor}$')
plt.show()

# Generate a picture of colonies with best locations marked
plt.figure(figsize=(8, 8))
plt.imshow(picture[:,:], cmap = 'gist_yarg')
xs = []
ys = []
for i in range(10):
    xpos = scipy.ndimage.center_of_mass(picture, colonies[0], sel[-1-i])[0]
    ypos = scipy.ndimage.center_of_mass(picture, colonies[0], sel[-1-i])[1]
    xs.append(xpos)
    ys.append(ypos)
    plt.annotate(
        i+1,
        alpha=0.5,
        color = 'b',
        xy = (ypos,xpos), xytext = (-5, 5),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
c = plt.scatter(ys,xs, color = 'r')
c.set_alpha(0.25)
plt.axis("off")
plt.title('Colony Selection from Plate: ' + plate_name + ', at ' + datestr)
plt.show()

# Offer exit dialog
imageOK = tkMessageBox.askyesno('Option','Pick Colonies?') # Dialog box: Do you want to continue?
print "here"
print imageOK
if not(imageOK):
    sys.exit()



for i in range(5):
    picker.pickNextBead()
    xpos = (scipy.ndimage.center_of_mass(picture, colonies[0], sel[-1-i])[0])
    ypos = (scipy.ndimage.center_of_mass(picture, colonies[0], sel[-1-i])[1])
    print xpos, ypos
    pos = transformation.transform([[xpos,ypos]])[0]
    print xpos, ypos,pos
    picker.pickColony(pos)
    picker.innoculateNextWell()

picker.home()


    
