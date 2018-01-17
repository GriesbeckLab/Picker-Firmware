import robot
import analyzer
import transformation
import numpy
import math
import scipy.ndimage
import skimage.measure

colonyCoordinate1=[-49.1,33.7] 
colonyCoordinate2=[-47.1,35.7]
colonyCoordinate3=[-47.1,35.7]

image = numpy.load('colonies.npy')
objects = analyzer.process_image(image)
positions = numpy.array(analyzer.get_positions(objects))



params = (2.1163087380926116, 0.080631675816675547, numpy.array([ 793.,  526.]), numpy.array([-53.22,  28.42]))

print positions
pos = transformation.transform(positions, params)
print pos 


for i in range(len(positions)/2, len(positions)/2 + 3):
    print pos[i]
'''

pl = robot.picker()
pl.connect()
pl.home()






pl.home()

'''
