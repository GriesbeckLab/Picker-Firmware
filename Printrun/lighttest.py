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




filters = ["485","505","535","570","600","630","712"]
lights = ["royalblue","blue","cyan","green","white","red","red"]


picker = robot.picker()
picker.connect()

for i in range(10):

    picker.lightOn(lights[0])
    time.sleep(1)
    picker.lightOff(lights[0])
    time.sleep(1)






