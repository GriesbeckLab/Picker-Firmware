import robot
import numpy
import math

picker = robot.picker()

picker.connect()
picker.home()

for x in range (0, 20):

    picker.pickNextBead()

    picker.innoculateNextWell()
