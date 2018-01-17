import math
import numpy

#param = (2.114659893497348, 0.074083856465594858, array([ 734.69565217,  529.76086957]), array([-48.13043478,  27.69565217]))

def getAngle(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    inner_product = x1*x2 + y1*y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    return math.acos(inner_product/(len1*len2))

def rotatePoint(point, theta):
    """docstring for rotate"""
    cs = math.cos(theta)
    sn = math.sin(theta)
    px = point[0] * cs - point[1] * sn
    py = point[0] * sn + point[1] * cs
    return (px, py)


def findCentroid(triangle):
    """The centroid of a finite set of points the arerage of each set of orthanogal point"""
    centroid = numpy.mean(triangle, axis=0)
    return centroid

def findScaleFactor(pointsA,pointsB):
    """Finds the length between points within a set, and gets the average ratio of the lengths between sets"""
    pointsA_rotated = numpy.vstack((pointsA[1:,:], pointsA[0,:]))-pointsA
    pointsB_rotated = numpy.vstack((pointsB[1:,:], pointsB[0,:]))-pointsB
    scale = numpy.mean(numpy.sqrt(numpy.square(pointsB_rotated[:,0])+numpy.square(pointsB_rotated[:,1]))/numpy.sqrt(numpy.square(pointsA_rotated[:,0])+numpy.square(pointsA_rotated[:,1])))
    return scale

def translate(l,c):
    """docstring for translate"""
    v = []
    for i in range(len(l)):
        p = [[],[]]
        p[0] = l[i][0] - c[0]
        p[1] = l[i][1] - c[1]
        v.append(p)
    return v

def findAngle(L1, L2):
    """docstring for center"""
    L1C = findCentroid(L1)
    L2C = findCentroid(L2)
    L1T = translate(L1,L1C)
    L2T = translate(L2,L2C)
    angle1 = getAngle(L1T[0],L2T[0])
    angle2 = getAngle(L1T[1],L2T[1])
    angle3 = getAngle(L1T[2],L2T[2])
    angle =  (angle1 + angle2 + angle3)/3
    return angle

def affineParams(L1, L2):
    R = findAngle(L1,L2)
    S = findScaleFactor(L1,L2)
    C1 = findCentroid(L1)
    C2 = findCentroid(L2)
    return (R,S,C1,C2)

def transform(L1, params):
    R = params[0]
    S = params[1]
    C1 = params[2]
    C2 = params[3]
    v = []
    for i in L1:
        p1 = [i[0]-C1[0], i[1]-C1[1]]
        p2 = rotatePoint(p1, -R)
        p3 = [p2[0]*S, p2[1]*S]
        p4 = [p3[0]+C2[0], p3[1]+C2[1]]
        v.append(p4)
    v = numpy.array(v)    
    return v


def transform(L1):
    v = []
    for i in L1:
        p = [ 0.0674*i[1] - 51.9 - 0.0424*i[0], 101 - 0.04*i[1] - 0.0699*i[0]]
        v.append(p)
    v = numpy.array(v)
    return v



if __name__ == '__main__':    
    #pic = numpy.array([[1003,50],[1164,305],[1053,233],[938,165],[821,97],[708,26],[1214,489],[1098,420],[983,351],[868,280],[752,210],[1143,605],[1029,534],[914,463],[798,395],[681,325],[566,255],[448,188],[1190,791],[1074,720],[958,649],[842,580],[725,510],[494,371],[377,301],[263,233],[1003,835],[887,765],[771,695],[656,626],[540,556],[424,487],[306,416],[933,950],[817,881],[700,812],[584,742],[470,670],[351,600],[237,532],[744,997],[629,926],[515,857],[398,787],[283,718],[444,971]])   
    #robot = numpy.array([[-89, 29], [-79, 9], [-79, 19], [-79, 29], [-79, 39], [-79, 49], [-69, -1], [-69, 9], [-69, 19], [-69, 29], [-69, 39],  [-59, -1], [-59, 9], [-59, 19], [-59, 29], [-59, 39], [-59, 49], [-59, 59], [-49, -11], [-49, -1], [-49, 9], [-49, 19], [-49, 29], [-49, 49], [-49, 59], [-49, 69], [-39, -1], [-39, 9], [-39, 19], [-39, 29], [-39, 39], [-39, 49], [-39, 59], [-29, -1], [-29, 9], [-29, 19], [-29, 29], [-29, 39], [-29, 49], [-29, 59], [-19, 9], [-19, 19], [-19, 29], [-19, 39], [-19, 49], [-9, 29]])  

    #pic = numpy.array([[980,90],[1070,447],[852,314],[639,182],[1157,799],[939,669],[724,537],[509,404],[294,272],[813,889,],[596,757],[381,626]])   
    
    #pic = numpy.array([[979,91],[1068,448],[852,314],[636,181],[1154,801],[938,669],[723,537],[509,405],[292,273],[811,889],[594,758],[382,626]])
    #robot = numpy.array([[-90, 28], [-80, 8], [-80, 18], [-80, 28], [-80, 38], [-80, 48], [-70, -2], [-70, 8], [-70, 18], [-70, 28], [-70, 38], [-70, 48], [-70, 58], [-60, -2], [-60, 8], [-60, 18], [-60, 28], [-60, 38], [-60, 48], [-60, 58], [-50, -12], [-50, -2], [-50, 8], [-50, 18], [-50, 28], [-50, 38], [-50, 48], [-50, 58], [-50, 68], [-40, -2], [-40, 8], [-40, 18], [-40, 28], [-40, 38], [-40, 48], [-40, 58], [-30, -2], [-30, 8], [-30, 18], [-30, 28], [-30, 38], [-30, 48], [-30, 58], [-20, 8], [-20, 18], [-20, 28], [-20, 38], [-20, 48], [-10, 28]])  
    #from numpy import genfromtxt
    #my_data = genfromtxt("coordinates_calibration.csv", delimiter=',')
    #pic = my_data[1:,2:4]
    #print pic

    robot = numpy.array([[-90, 28], [-80, 8], [-80, 18], [-80, 28], [-80, 38], [-80, 48], [-70, -2], [-70, 8], [-70, 18], [-70, 28], [-70, 38], [-70, 48], [-70, 58], [-60, -2], [-60, 8], [-60, 18], [-60, 28], [-60, 38], [-60, 48], [-60, 58], [-50, -12], [-50, -2], [-50, 8], [-50, 18], [-50, 28], [-50, 38], [-50, 48], [-50, 58], [-50, 68], [-40, -2], [-40, 8], [-40, 18], [-40, 28], [-40, 38], [-40, 48], [-40, 58], [-30, -2], [-30, 8], [-30, 18], [-30, 28], [-30, 38], [-30, 48], [-30, 58], [-20, 8], [-20, 18], [-20, 28], [-20, 38], [-20, 48], [-10, 28]])  

    pic = numpy.array([[982,87],[1135,333],[1029,266],[921,199],[815,132],[306,65],[1185,512],[1076,445],[967,379],[859,312],[750,245],[643,178],[534,111],[1120,623],[1011,557],[903,490],[795,424],[687,358],[579,291],[470,225],[1163,799],[1056,734],[947,668],[838,601],[729,535],[622,470],[514,404],[405,337],[298,270],[991,844],[882,778],[774,713],[666,646],[555,580],[448,514],[342,448],[927,954],[818,888],[709,822],[600,757],[493,692],[385,625],[276,560],[753,997],[644,931],[536,867],[428,802],[319,736],[471,976]])


    params = affineParams(pic,robot)
    out = transform(pic, params)

    #test = numpy.array([[635,141], [517,71],[610, 441]])
    #testout = transform(test, params)
    
    print params

    x = pic[:,0]
    y = pic[:,1]
    x1 = robot[:,0]
    y1 = robot[:,1]
    x2 = out[:,0]
    y2 = out[:,1]
    #x3 = testout[:,0]
    #y3 = testout[:,1]

    f = 78.7

    scalefactor = f/math.sqrt((robot[0][0] - robot[-1][0])**2 + (robot[0][1] - robot[-1][1])**2)
    print math.sqrt((robot[0][0] - robot[-1][0])**2 + (robot[0][1] - robot[-1][1])**2)
    print robot[0],robot[-1]
    error = []
    for i in range(len(out)):
        e = math.sqrt((robot[i][0] - out[i][0])**2 + (robot[i][1] - out[i][1])**2)*scalefactor
        error.append(e)
    print error

    err = numpy.array(error)
    print  "mean ", err.mean()
    print  "std ", err.std()
    print  "max ", err.max()

    import matplotlib.pyplot as plt

    #plt.scatter(x,y, color='r')
    plt.figure()
    plt.scatter(x1,y1, color='b')
    plt.scatter(x2,y2, color='g')
    #plt.scatter(x3,y3, color='y')
    plt.show()
    plt.show(block=False)

    from pylab import *
    figure()
    boxplot(err)
    
    show()
