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



picker = robot.picker()
picker.connect()
picker.home()
print "here"
#time.sleep(3)


#picker.moveToSafeHeight()
#while picker.connection.printing:
#            time.sleep(1)
#picker.park()
picker.homefilter()
time.sleep(3)


f = ['630', '570', '485', '535','485', '712', '505']
for i in f:
    print i
    picker.emission(i)
    time.sleep(5)
    

#picker.lightOn('white')
#time.sleep(1)
#picker.lightOff('white')



