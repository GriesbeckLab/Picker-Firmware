# imports vital stuff for imgae processing, getting the time and date, etc...
import PIL
import time
import sys
import scipy.misc
import numpy
import pylab as pl
import matplotlib.cm as cm

a = numpy.load('9-a.npy')
b = numpy.load('9-b.npy')

pl.imshow((b-a)+50, cmap='gray' )
pl.show()
