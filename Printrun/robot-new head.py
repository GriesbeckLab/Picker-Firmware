import time
import getopt
import sys
import math
import numpy as np
from printrun.printcore import printcore
from printrun import gcoder

class picker():
    def __init__(self):
        self.beadplateCorners = [[153.6, 19.0], [112.5, 112.6], [97.7, -4.0], [57.4, 90.1 ]] #Corner well positions of A1, A12, H1, H12
        self.beadplateShape = [12,8] #Layout
        self.beadplateLocations = []
        self.beadplateSafeHeight = 120 #140.0 befor nail cut
        self.beadHeight = 105.7  #126.0 befor nail cut

        self.deepwellCorners = [[-48.0, -153.0], [57.0, -145.0], [-53.0, -94.0], [50.0, -85.0]] #Corner well positions of A1, A12, H1, H12
        self.deepwellShape = [12,8] #Layout
        self.deepwellHeight = 143.0
        self.deepwellLocation = []

        self.beadTesterLocation = [54.0,-8.0,100.2]# get this location!!! [x,y,z]  original 79.3,132.5,122.6
        self.parkPosition = [100.0,-60.0,150.0]
        self.safeHeight = 155.0  

        self.LEDs = {'royalblue': "11",'blue': "28", 'cyan': "10", 'green': "29", 'amber': "17", 'red': "30", 'white': "16"}                  
        self.filters = {'712':'0', '630':'29', '600':'62', '570':'92', '535':'119', '505':'145','485': "173"}
        self.port = "COM6"
        self.baud = 115200
        self.connection = None
        self.beadplateState = [True]*self.beadplateShape[0]*self.beadplateShape[1] #All bead postions full at beginning

        print self.beadplateState
        
        
        self.deepwellState = [False]*self.deepwellShape[0]*self.deepwellShape[1] #All well postions empty at beginning
        
        def rotation(points):
            """Calculates the rotation of the plate from the top two plate points"""
            deltaX1 = points[1][0] - points[0][0]
            deltaY1 = points[1][1] - points[0][1]
            deltaX2 = points[3][0] - points[2][0]
            deltaY2 = points[3][1] - points[2][1]

            #print math.atan(deltaY1/deltaX1), math.atan(deltaY2/deltaX2)
            avg = (math.atan(deltaY1/deltaX1) + math.atan(deltaY2/deltaX2))/2
            return avg

        def spacing(points, shape):
            """Calculates the spacing of the wells from the top two plate points in x and y offsets"""
            x1Distance = math.sqrt((points[1][0] - points[0][0])**2 + (points[1][1] - points[0][1])**2)/(shape[0]-1) 
            y1Distance = math.sqrt((points[2][0] - points[0][0])**2 + (points[2][1] - points[0][1])**2)/(shape[1]-1)
            x2Distance = math.sqrt((points[3][0] - points[2][0])**2 + (points[3][1] - points[2][1])**2)/(shape[0]-1) 
            y2Distance = math.sqrt((points[3][0] - points[1][0])**2 + (points[3][1] - points[1][1])**2)/(shape[1]-1)

            print('x distances')
            print x1Distance, x2Distance

            print('y distances')
            print y1Distance, y2Distance
            return (x1Distance + x2Distance)/2, y2Distance

        def transformPoint(point, rotation, origin):
            """Rotates well location around A1 well location"""
            if rotation >= 0:
                dx = origin[0] + (math.cos(rotation)*point[0] - math.sin(rotation)*point[1])
                dy = origin[1] + (math.sin(rotation)*point[0] + math.cos(rotation)*point[1])
            else:
                dx = origin[0] - (math.cos(rotation)*point[0] - math.sin(rotation)*point[1])
                dy = origin[1] - (math.sin(rotation)*point[0] + math.cos(rotation)*point[1])
            print  dx,dy   
            return dx,dy
        
        def transformGrid(corners, shape):
            """Uses the corners locations and shape of the plate to determine the location of the wells"""
            plateRotation = rotation(corners)
            plateSpacing = spacing(corners, shape)
            location = []
        
            for i in range(shape[1]):
                for j in range(shape[0]):
                    point = [j*plateSpacing[0],i*plateSpacing[1]]
                    transformedPoint = transformPoint(point, plateRotation, corners[0])
                    location.append(transformedPoint)
            return location

        def transformGrid1(corners, shape):
            """Uses the corners locations and shape of the plate to determine the location of the wells"""
            #self.beadplateCorners = [[152.8, 18.7], [112.3, 112.6], [96.8, -4.5], [56.8, 89.0 ]] #Corner well positions of A1, A12, H1, H12
            #self.beadplateShape = [12,8] #Layout
            xp1 = np.linspace(corners[0][0], corners[2][0], shape[1])
            yp1 = np.linspace(corners[0][1], corners[2][1], shape[1])

            xp2 = np.linspace(corners[1][0], corners[3][0], shape[1])
            yp2 = np.linspace(corners[1][1], corners[3][1], shape[1])

            xx = np.array([])
            yy = np.array([])
            for i in range(8):
                    xtemp = np.linspace(xp1[i], xp2[i], shape[0])
                    xx = np.append(xx, xtemp)
                    ytemp = np.linspace(yp1[i], yp2[i], shape[0])
                    yy = np.append(yy, ytemp)
            location = []        
            for i in range(len(xx)):
                point = xx[i], yy[i]
                location.append(point)
            return location


        
        self.beadplateLocations = self.beadplateCorners
        self.beadplateLocations = transformGrid1(self.beadplateCorners, self.beadplateShape)
        print self.beadplateLocations
        
        self.deepwellLocation = transformGrid(self.deepwellCorners, self.deepwellShape)
        
        
    def connect(self):
        """docstring for connect"""
        print("Connecting...")
        self.connection = printcore(self.port, self.baud)
        self.connection.loud = True
        time.sleep(2)
        self.connection.send_now("G90")
    
    def disconnect(self):
        """docstring for disconnect"""
        self.connection.disconnect()
        time.sleep(2)
   
    def runGCode(self, code):
        gcode = code
        gcode.append("M114")
        gcode = gcoder.GCode(code)
        self.connection.startprint(gcode)
        while self.connection.printing:
            time.sleep(0.1)

    def home(self):
        """Moves the picker to the home position"""
        self.runGCode(["G28"])

    def state(self):
        print(self.connection.mainqueue)
        
    def park(self):
        """Moves the picker to the imaging position"""
        print("Parking Picker Head")
        self.runGCode(["G1 X" + str(self.parkPosition[0]) + " Y" + str(self.parkPosition[1]) + " Z" + str(self.parkPosition[2])])           

    def move(self, x, y, z=167.0, s=15000.0):
        """Move to X,Y,Z at speed S"""
        self.runGCode(["G1 X" + str(x) + " Y" + str(y) + " Z" + str(z) + " F" + str(s)])

    def moveToSafeHeight(self):
        """Move to X,Y,Z at speed S"""
        self.runGCode(["G1 Z" + str(self.safeHeight) + " F" + str(15000.0)])
        
    def nextBead(self):
        """return the position ofself.safeHeight the next free bead, or false if there are no free beads left"""
        print('next bead')
        print (self.beadplateState.index(True) if True in self.beadplateState else None)
        return (self.beadplateState.index(True) if True in self.beadplateState else None)                
      
    def nextWell(self):
        """docstring for nextWell"""
        return (self.deepwellState.index(False) if False in self.deepwellState else None)

    def testBead(self):
        """docstring for testBead"""
        self.move(self.beadTesterLocation[0],self.beadTesterLocation[1],self.beadplateSafeHeight)
        self.move(self.beadTesterLocation[0],self.beadTesterLocation[1],self.beadTesterLocation[2])
        self.dropBead()
        time.sleep(1) #Settling time
        self.runGCode(["M119"]) #Get endstops
        self.pickBead()
        self.move(self.beadTesterLocation[0],self.beadTesterLocation[1],self.beadplateSafeHeight)

    def pickBead(self):
        """docstring for pickBead"""
        self.runGCode(["M106 S255"])

    def dropBead(self):
        """docstring for pickBead"""
        self.runGCode(["M107"])
        self.connection.contact = False
        
    def pickNextBead(self):
        """docstring for pickNextBead"""
        self.moveToSafeHeight()
        position = self.nextBead()
        if position == None:
            return fail
        success = False
        print "Here", self.beadplateState[position]
        while self.beadplateState[position]:
            tries = 1
            while tries > 0:
                self.moveToSafeHeight()
                self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1])
                self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1],z = self.beadplateSafeHeight)
                self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1],z = self.beadHeight, s = 500)
                time.sleep(0.5)
                self.pickBead()
                self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1],z = self.beadplateSafeHeight)
                self.testBead()

                print "Bead in place: "
                if self.connection.contact:
                    success = True
                    print 'success'
                    break
                else:
                    print 'fail'
                    self.moveToSafeHeight()
                    self.move(self.parkPosition[0],self.parkPosition[1],self.parkPosition[2])
                    self.dropBead()
                    tries = tries - 1

            self.beadplateState[position] = False
                    
            if success == True:
                break
            else:
                position = self.nextBead()
        return success       


    def testBeadPlate(self):
        """docstring for pickNextBead"""
        self.moveToSafeHeight()
        position = self.nextBead()
        if position == None:
            return fail
        success = False
        print "Here", self.beadplateState[position]
        while self.beadplateState[position]:
            print self.beadplateLocations[position][0],self.beadplateLocations[position][1]
            self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1],z = self.beadplateSafeHeight)
            self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1],z = self.beadHeight + 8, s = 500)
            time.sleep(0.5)
            self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1],z = self.beadplateSafeHeight)

            self.beadplateState[position] = False
            position = self.nextBead()
            
        return success

    
    def testDrop(self):
        # currently not used
        self.move(x=-50.0,y=31.0,z = 170.0, s = 15000)
        self.move(x=-43.0,y=-153.0,z = 170.0) 
        self.dropBead()
        time.sleep(0.5)
   
        
    def innoculateWell(self, n):
        """docstring for innoculateWell"""
        pass
        
    def innoculateNextWell(self):
        """docstring for innoculateNextWell"""
        self.moveToSafeHeight()
        position = self.nextWell()
        if position == None:
            return fail
            success = False
        print "Here", self.deepwellState[position]
        
        self.moveToSafeHeight()
        self.move(x=self.deepwellLocation[position][0],y=self.deepwellLocation[position][1])
        self.move(x=self.deepwellLocation[position][0],y=self.deepwellLocation[position][1],z = self.deepwellHeight)
                             
        self.dropBead()
        time.sleep(0.5)
        self.moveToSafeHeight()
                       
        self.deepwellState[position] = True
        success = True            
        return success 

    def setbeadplateState(self, n):
        self.beadplateState[n] = False
        """docstring for set"""
        pass
        
    def setdeepwellState(self, n):
        self.deepwellState[n] = True
        """docstring for fname"""
        pass
    
    def pickColony(self, colonyCoordinate):
        """docstring for pickColony"""
        self.moveToSafeHeight()
        self.move(colonyCoordinate[0],colonyCoordinate[1])
        self.move(colonyCoordinate[0],colonyCoordinate[1],z=100.0) #moves to save hight above plate
        self.runGCode(["G30"])
        self.connection.contact = False
        self.moveToSafeHeight()

    def lightOn(self, color = "white", t = 0.1):
        """docstring for pickColony"""
        self.runGCode(["M42 P" + self.LEDs[color] + " S255"]) #M42 P16 S255

    def lightOff(self, color = "white"):
        """docstring for pickColony"""
        self.runGCode(["M42 P" + self.LEDs[color] + " S0"]) #M42 P16 S255

    def emission(self, wavelength = "485"):
        self.runGCode(["G1 E" + self.filters[wavelength] + " F4000", "M114"])           

    def placeBead(self, x, y):
        pass

    def homefilter(self):
        self.connection.calibrate = []
        self.runGCode([ "G92 E0", "G1 E 0  F2000", "M119", "G1 E 1  F2000", "M119", "G1 E 2  F2000", "M119", "G1 E 3  F2000", "M119", "G1 E 4  F2000", "M119", "G1 E 5  F2000", "M119", "G1 E 6  F2000", "M119", "G1 E 7  F2000", "M119", "G1 E 8  F2000", "M119", "G1 E 9  F2000", "M119", "G1 E 10  F2000", "M119", "G1 E 11  F2000", "M119", "G1 E 12  F2000", "M119", "G1 E 13  F2000", "M119", "G1 E 14  F2000", "M119", "G1 E 15  F2000", "M119", "G1 E 16  F2000", "M119", "G1 E 17  F2000", "M119", "G1 E 18  F2000", "M119", "G1 E 19  F2000", "M119", "G1 E 20  F2000", "M119", "G1 E 21  F2000", "M119", "G1 E 22  F2000", "M119", "G1 E 23  F2000", "M119", "G1 E 24  F2000", "M119", "G1 E 25  F2000", "M119", "G1 E 26  F2000", "M119", "G1 E 27  F2000", "M119", "G1 E 28  F2000", "M119", "G1 E 29  F2000", "M119", "G1 E 30  F2000", "M119", "G1 E 31  F2000", "M119", "G1 E 32  F2000", "M119", "G1 E 33  F2000", "M119", "G1 E 34  F2000", "M119", "G1 E 35  F2000", "M119", "G1 E 36  F2000", "M119", "G1 E 37  F2000", "M119", "G1 E 38  F2000", "M119", "G1 E 39  F2000", "M119", "G1 E 40  F2000", "M119", "G1 E 41  F2000", "M119", "G1 E 42  F2000", "M119", "G1 E 43  F2000", "M119", "G1 E 44  F2000", "M119", "G1 E 45  F2000", "M119", "G1 E 46  F2000", "M119", "G1 E 47  F2000", "M119", "G1 E 48  F2000", "M119", "G1 E 49  F2000", "M119", "G1 E 50  F2000", "M119", "G1 E 51  F2000", "M119", "G1 E 52  F2000", "M119", "G1 E 53  F2000", "M119", "G1 E 54  F2000", "M119", "G1 E 55  F2000", "M119", "G1 E 56  F2000", "M119", "G1 E 57  F2000", "M119", "G1 E 58  F2000", "M119", "G1 E 59  F2000", "M119", "G1 E 60  F2000", "M119", "G1 E 61  F2000", "M119", "G1 E 62  F2000", "M119", "G1 E 63  F2000", "M119", "G1 E 64  F2000", "M119", "G1 E 65  F2000", "M119", "G1 E 66  F2000", "M119", "G1 E 67  F2000", "M119", "G1 E 68  F2000", "M119", "G1 E 69  F2000", "M119", "G1 E 70  F2000", "M119", "G1 E 71  F2000", "M119", "G1 E 72  F2000", "M119", "G1 E 73  F2000", "M119", "G1 E 74  F2000", "M119", "G1 E 75  F2000", "M119", "G1 E 76  F2000", "M119", "G1 E 77  F2000", "M119", "G1 E 78  F2000", "M119", "G1 E 79  F2000", "M119", "G1 E 80  F2000", "M119", "G1 E 81  F2000", "M119", "G1 E 82  F2000", "M119", "G1 E 83  F2000", "M119", "G1 E 84  F2000", "M119", "G1 E 85  F2000", "M119", "G1 E 86  F2000", "M119", "G1 E 87  F2000", "M119", "G1 E 88  F2000", "M119", "G1 E 89  F2000", "M119", "G1 E 90  F2000", "M119", "G1 E 91  F2000", "M119", "G1 E 92  F2000", "M119", "G1 E 93  F2000", "M119", "G1 E 94  F2000", "M119", "G1 E 95  F2000", "M119", "G1 E 96  F2000", "M119", "G1 E 97  F2000", "M119", "G1 E 98  F2000", "M119", "G1 E 99  F2000", "M119", "G1 E 100  F2000", "M119", "G1 E 101  F2000", "M119", "G1 E 102  F2000", "M119", "G1 E 103  F2000", "M119", "G1 E 104  F2000", "M119", "G1 E 105  F2000", "M119", "G1 E 106  F2000", "M119", "G1 E 107  F2000", "M119", "G1 E 108  F2000", "M119", "G1 E 109  F2000", "M119", "G1 E 110  F2000", "M119", "G1 E 111  F2000", "M119", "G1 E 112  F2000", "M119", "G1 E 113  F2000", "M119", "G1 E 114  F2000", "M119", "G1 E 115  F2000", "M119", "G1 E 116  F2000", "M119", "G1 E 117  F2000", "M119", "G1 E 118  F2000", "M119", "G1 E 119  F2000", "M119", "G1 E 120  F2000", "M119", "G1 E 121  F2000", "M119", "G1 E 122  F2000", "M119", "G1 E 123  F2000", "M119", "G1 E 124  F2000", "M119", "G1 E 125  F2000", "M119", "G1 E 126  F2000", "M119", "G1 E 127  F2000", "M119", "G1 E 128  F2000", "M119", "G1 E 129  F2000", "M119", "G1 E 130  F2000", "M119", "G1 E 131  F2000", "M119", "G1 E 132  F2000", "M119", "G1 E 133  F2000", "M119", "G1 E 134  F2000", "M119", "G1 E 135  F2000", "M119", "G1 E 136  F2000", "M119", "G1 E 137  F2000", "M119", "G1 E 138  F2000", "M119", "G1 E 139  F2000", "M119", "G1 E 140  F2000", "M119", "G1 E 141  F2000", "M119", "G1 E 142  F2000", "M119", "G1 E 143  F2000", "M119", "G1 E 144  F2000", "M119", "G1 E 145  F2000", "M119", "G1 E 146  F2000", "M119", "G1 E 147  F2000", "M119", "G1 E 148  F2000", "M119", "G1 E 149  F2000", "M119", "G1 E 150  F2000", "M119", "G1 E 151  F2000", "M119", "G1 E 152  F2000", "M119", "G1 E 153  F2000", "M119", "G1 E 154  F2000", "M119", "G1 E 155  F2000", "M119", "G1 E 156  F2000", "M119", "G1 E 157  F2000", "M119", "G1 E 158  F2000", "M119", "G1 E 159  F2000", "M119", "G1 E 160  F2000", "M119", "G1 E 161  F2000", "M119", "G1 E 162  F2000", "M119", "G1 E 163  F2000", "M119", "G1 E 164  F2000", "M119", "G1 E 165  F2000", "M119", "G1 E 166  F2000", "M119", "G1 E 167  F2000", "M119", "G1 E 168  F2000", "M119", "G1 E 169  F2000", "M119", "G1 E 170  F2000", "M119", "G1 E 171  F2000", "M119", "G1 E 172  F2000", "M119", "G1 E 173  F2000", "M119", "G1 E 174  F2000", "M119", "G1 E 175  F2000", "M119", "G1 E 176  F2000", "M119", "G1 E 177  F2000", "M119", "G1 E 178  F2000", "M119", "G1 E 179  F2000", "M119", "G1 E 180  F2000", "M119", "G1 E 181  F2000", "M119", "G1 E 182  F2000", "M119", "G1 E 183  F2000", "M119", "G1 E 184  F2000", "M119", "G1 E 185  F2000", "M119", "G1 E 186  F2000", "M119", "G1 E 187  F2000", "M119", "G1 E 188  F2000", "M119", "G1 E 189  F2000", "M119", "G1 E 190  F2000", "M119", "G1 E 191  F2000", "M119", "G1 E 192  F2000", "M119", "G1 E 193  F2000", "M119", "G1 E 194  F2000", "M119", "G1 E 195  F2000", "M119", "G1 E 196  F2000", "M119", "G1 E 197  F2000", "M119", "G1 E 198  F2000", "M119", "G1 E 199  F2000", "M119"])
        homepoint = 0        
        for i in range(len(self.connection.calibrate)):
            if self.connection.calibrate[i][-10:-1] == "TRIGGERED":
                homepoint = i
                break
        print "Homepoint = ", homepoint

        self.runGCode([ "G1 E" + str(homepoint) + "F4000", "G92 E173"]) #E0 before
        self.connection.calibrate = []

    def calibrate(self): # redundant
        self.moveToSafeHeight()
        locations = [[-85.0, 36.0],[-60.0,66.0],[-60.0,11.0],[-29.0,21.0],[-29.0,51.0]]
        for point in locations:
            self.pickNextBead()
            self.moveToSafeHeight()
            self.move(x=point[0],y=point[1])
            self.move(x=point[0],y=point[1], z=100.0)
            self.runGCode(["G30","G91","G1 Z3","G90"])
            self.dropBead()

if __name__ == '__main__':

    p = picker()
    p.connect()
    if p.connection.online:
        p.home()
        p.dropBead()
        #p.homefilter()
        #p.calibrate()
        p.testBeadPlate()
        '''
        p.lightOn('white')
        p.lightOff('white')
        p.lightOn('royalblue')
        p.lightOff('royalblue')
        p.lightOn('blue')
        p.lightOff('blue') 
        p.lightOn('cyan')
        p.lightOff('cyan')
        p.lightOn('green')
        p.lightOff('green')
        p.lightOn('amber')
        p.lightOff('amber')
        p.lightOn('red')
        p.lightOff('red')
        p.moveToSafeHeight()
        '''
        '''
        print p.beadplateState
        while p.nextBead() != None:
            position = p.nextBead()
            p.move(x=p.beadplateLocations[position][0],y=p.beadplateLocations[position][1],z = p.beadplateSafeHeight)
            time.sleep(0.25)
            p.beadplateState[position] = False
            print p.beadplateState
        p.moveToSafeHeight()
        p.park()
        p.pickNextBead()
        '''
        p.testDrop()
        p.move(100.0,-60.0,150.0)
        p.home()
        
        print p.beadplateState
        p.disconnect()
