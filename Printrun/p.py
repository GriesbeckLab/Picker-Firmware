import robot as p

robot = p.picker()
robot.connect()
if robot.connection.online:
    robot.home()
    robot.lightOn('white', 0.2) #self.LEDs = {'royalblue': "11", 'cyan': "28", 'blue': "10", 'green': "29", 'amber': "17", 'red': "30", 'white': "16"}
    robot.lightOn('blue', 0.2)
    robot.lightOn('cyan', 0.2)
    robot.lightOn('green', 0.2)
    robot.lightOn('amber', 0.2)
    robot.lightOn('royalblue', 0.2)
    robot.lightOn('red', 0.2)
    robot.moveToSafeHeight()
    #p.park()
    #p.pickNextBead()
    #p.testDrop()
    #p.home()
    #print p.beadplateState
    robot.disconnect()
