import time
import getopt
import sys
import math
from printrun.printcore import printcore
from printrun import gcoder

class picker():
    def __init__(self):
        self.beadplateCorners = [[151.0, 23.0], [115.0, 111.0], [93.0, -3.0], [57.0, 86.0]] #Corner well positions of A1, A12, H1, H12
        self.beadplateShape = [12,8] #Layout
        self.beadplateLocations = []
        self.beadplateSafeHeight = 140
        self.beadHeight = 126.0
        
        self.deepwellCorners = [[-43.0, -153.0], [52.0, -144.0], [-49.0, -90.0], [46.0, -81.0]] #Corner well positions of A1, A12, H1, H12
        self.deepwellShape = [12,8] #Layout
        self.deepwellHeight = 100#
        self.deepwellLocation = []
        
        self.beadTesterLocation = [79.3,132.5,126.6]# get this location!!! [x,y,z]
        self.parkPosition = [108,-62,182]
        self.safeHeight = 167.0
        
        
        self.port = "COM3"
        self.baud = 115200
        self.connection = None
        self.beadplateState = [True]*self.beadplateShape[0]*self.beadplateShape[1] #All bead postions full at beginning
        self.deepwellState = [False]*self.deepwellShape[0]*self.deepwellShape[1] #All well postions empty at beginning

        def rotation(points):
            """Calculates the rotation of the plate from the top two plate points"""
            deltaX = points[1][0] - points[0][0]
            deltay = points[1][1] - points[0][1]
            return math.atan(deltay/deltaX)

        def spacing(points, shape):
            """Calculates the spacing of the wells from the top two plate points in x and y offsets"""
            xDistance = math.sqrt((points[1][0] - points[0][0])**2 + (points[1][1] - points[0][1])**2)/(shape[0]-1)
            yDistance = math.sqrt((points[2][0] - points[0][0])**2 + (points[2][1] - points[0][1])**2)/(shape[1]-1)
            return xDistance, yDistance

        def transformPoint(point, rotation, origin):
            """Rotates well location around A1 well location"""
            if rotation >= 0:
                dx = origin[0] + (math.cos(rotation)*point[0] - math.sin(rotation)*point[1])
                dy = origin[1] + (math.sin(rotation)*point[0] + math.cos(rotation)*point[1])
            else:
                dx = origin[0] - (math.cos(rotation)*point[0] - math.sin(rotation)*point[1])
                dy = origin[1] - (math.sin(rotation)*point[0] + math.cos(rotation)*point[1])    
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
            
        self.beadplateLocations = transformGrid(self.beadplateCorners, self.beadplateShape)
        self.deepwellLocation = transformGrid(self.deepwellCorners, self.deepwellShape)
        
        
    def connect(self):
        """docstring for connect"""
        print("Connecting...")
        self.connection = printcore(self.port, self.baud)
        self.connection.loud = True
        time.sleep(2)
    
    def disconnect(self):
        """docstring for disconnect"""
        self.connection.disconnect()
        time.sleep(2)
        pass    
    
    def home(self):
        """Moves the picker to the home position"""
        code = ["G28"]
        code = gcoder.GCode(code)
        p.connection.startprint(code)
        while p.connection.printing:
            time.sleep(1)

    def state(self):
        print(self.connection.mainqueue)

        
    def park(self):
        """Moves the picker to the imaging position"""
        print("parking")
        self.move(self.parkPosition[0], self.parkPosition[1], self.parkPosition[2])
        time.sleep(1)

    def move(self, x, y, z=167.0, s=9000.0):
        """Move to X,Y,Z at speed S"""
        locationString =  "G1 X" + str(x) + " Y" + str(y) + " Z" + str(z) + " F" + str(s)
        return locationString
        

    def moveToSafeHeight(self):
        """Move to X,Y,Z at speed S"""
        path =  ["G1 Z" + str(self.safeHeight) + " F" + str(5000.0)]
        path = gcoder.GCode(path)
        p.connection.startprint(path)
        while p.connection.printing:
            pass#time.sleep(1)
        
    def nextBead(self):
        """return the position ofself.safeHeight the next free bead, or false if there are no free beads left"""
        return (self.beadplateState.index(True) if True in self.beadplateState else None)                
      
    def nextWell(self):
        """docstring for nextWell"""
        return (self.deepwellState.index(True) if True in self.deepwellState else None)

    def testBead(self):
        """docstring for testBead"""
        path = []
        path.append(self.move(self.beadTesterLocation[0],self.beadTesterLocation[1],self.beadplateSafeHeight, s = 9000))
        path.append(self.move(self.beadTesterLocation[0],self.beadTesterLocation[1],self.beadTesterLocation[2], s = 9000))
        path = gcoder.GCode(path)
        p.connection.startprint(path)
        while p.connection.printing:
            time.sleep(0.1)
            
        self.dropBead()
        time.sleep(0.5)

        code = ["M119"]
        code = gcoder.GCode(code)
        p.connection.startprint(code)
        while p.connection.printing:
            time.sleep(0.1)
            


        self.pickBead()
        print p.connection.contact
        path = []
        path.append(self.move(self.beadTesterLocation[0],self.beadTesterLocation[1],self.beadplateSafeHeight, s = 9000))
        path = gcoder.GCode(path)
        p.connection.startprint(path)
        while p.connection.printing:
            time.sleep(0.1)
        state = p.connection.contact



    def pickBead(self):
        """docstring for pickBead"""
        code = ["M106 S255"]
        code = gcoder.GCode(code)
        p.connection.startprint(code)
        while p.connection.printing:
            time.sleep(0.1)
        time.sleep(1)  

    def dropBead(self):
        """docstring for pickBead"""
        code = ["M107"]
        code = gcoder.GCode(code)
        p.connection.startprint(code)
        while p.connection.printing:
            time.sleep(0.1)
        
    def pickNextBead(self):
        """docstring for pickNextBead"""
        path = []
        position = self.nextBead()

        self.moveToSafeHeight()

        path.append(self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1]))
        path.append(self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1],z = self.beadplateSafeHeight))
        path.append(self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1],z = self.beadHeight, s = 500))
        path = gcoder.GCode(path)
        p.connection.startprint(path)
        while p.connection.printing:
            time.sleep(0.1)
                
        self.pickBead()
        path = []        
        path.append(self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1],z = self.beadplateSafeHeight))
        path = gcoder.GCode(path)
        p.connection.startprint(path)
        while p.connection.printing:
            time.sleep(0.1)
                
        print "Result:"
        self.testBead()

        print "p.connection.contact:"
        print p.connection.contact
        path = []
        
        path.append(self.move(x=self.beadplateLocations[position][0],y=self.beadplateLocations[position][1],z = self.beadplateSafeHeight, s = 9000))
        path = gcoder.GCode(path)
        p.connection.startprint(path)
        while p.connection.printing:
            time.sleep(0.1)
            
        self.dropBead()
        time.sleep(0.5)
   
        
    def innoculateWell(self, n):
        """docstring for innoculateWell"""
        pass
        
    def innoculateNextWell(self):
        """docstring for innoculateNextWell"""
        pass    

    def setbeadplateState(self, n):
        self.beadplateState[n] = False
        """docstring for set"""
        pass
        
    def setdeepwellState(self, n):
        self.deepwellState[n] = True
        """docstring for fname"""
        pass
    
    def pickColony(self, x, y):
        """docstring for pickColony"""
        pass    
        
            

if __name__ == '__main__':



    p = picker()
    p.connect()
    if p.connection.online:
        p.home()
        p.moveToSafeHeight()
        #p.park()
        p.pickNextBead()
        p.home()
        p.disconnect()
