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



picker = robot.picker()
picker.connect()
picker.home()

center = [-50,28]
points = []
for x in range(-20,20,20):
    for y in range(-20,20,20):
        if math.sqrt(x**2 + y**2) <= 40:
        	points.append([x,y])
print points
print len(points)   

picker.moveToSafeHeight()
picker.park()

picker.lightOn('white')
time.sleep(1)
picker.lightOff('white')

picker.lightOn('blue')
time.sleep(1)
picker.lightOff('blue')

picker.lightOn('cyan')
time.sleep(1)
picker.lightOff('cyan')

picker.lightOn('green')
time.sleep(1)
picker.lightOff('green')

picker.lightOn('amber')
time.sleep(1)
picker.lightOff('amber')

picker.pickNextBead()

for point in points:
    #picker.pickNextBead()
    #picker.park()
    picker.moveToSafeHeight()
    time.sleep(0.2)
    picker.move(point[0]+center[0], point[1]+center[1])
    time.sleep(0.2)
    picker.move(point[0]+center[0], point[1]+center[1], 87.0)
    #picker.dropBead()
    time.sleep(1)
    picker.moveToSafeHeight()
    time.sleep(0.2)
    
picker.innoculateNextWell()
picker.home()
''' 
                
while picker.connection.printing:
            time.sleep(0.1)


picker.lightOn('white')
image = snapImage(5)
picker.lightOff('white')

pl.figure()
pl.imshow(image)
pl.show()

objects = analyzer.process_image(image)
positions = numpy.array(analyzer.get_positions(objects))
params = (2.113487776997974, 0.073996640890684487, numpy.array([ 684.0,  487.71428571]), numpy.array([-49.02857143,  32.65714286]))
pos = transformation.transform(positions, params)

pl.figure()
pl.imshow(objects)
pl.show()

picker.home()

for i in range(len(objects)):
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

xs = []
ys = []
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




pl.figure
pl.imshow(objects, cmap='gray')
pl.show()
'''
