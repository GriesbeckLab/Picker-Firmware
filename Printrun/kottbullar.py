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
picker.home()

picker.moveToSafeHeight()
picker.park()
while picker.connection.printing:
            time.sleep(0.1)

picker.lightOn('white')
image = snapImage(5)
picker.lightOff('white')

pl.figure()
pl.imshow(image)
pl.show()

#objects = analyzer.process_image(image)
positions = numpy.array([[916,80],[586,702],[685,969]])
#positions = numpy.array(analyzer.get_positions(objects))

pos = transformation.transform(positions)

#pl.figure()
#pl.imshow(objects)
#pl.show()

picker.home()

for i in range(len(pos)):
    picker.pickNextBead()
    while picker.connection.printing:
            time.sleep(0.1)
    picker.pickColony(pos[i])
    while picker.connection.printing:
            time.sleep(0.1)
    picker.innoculateNextWell()
    while picker.connection.printing:
            time.sleep(0.1)
            
picker.home()
'''
xs = []
ys = []3
for i in range(len(positions)):
    xpos = positions[i][0]
    ypos = positions[i][1]
    xs.append(xpos)
    ys.append(ypos)
    pl.annotate(
        i+1,
        alpha=0.5,
        color = 'y',
        xy = (ypos,xpos), xytext = (-5, 5),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
c = pl.scatter(ys,xs, color = 'r')
c.set_alpha(0.25)
pl.axis("off")
#pl.title('Colony Selection from Plate: ' + plate_name + ', at ' + datestr)




#pl.figure
#pl.imshow(objects, cmap='gray')
#pl.show()
'''
