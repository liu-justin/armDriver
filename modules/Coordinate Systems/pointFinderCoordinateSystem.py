# import modules.basicShapes as bs
# import modules.weightManager as wm
import CoordinateSystemConstants as csc
import Point as p
import turtle
import math
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def findAngle2D(csm, test):
    # # renaming variables for the equation in the notebook
    x = test.x
    y = test.y # y is up
    z = test.z
    rR = math.sqrt(csc.RC.x**2 + csc.RC.y**2)
    rC = math.sqrt(csc.CE.x**2 + csc.CE.y**2)

    angleRotation = math.atan2(y,x)
    # working in the XY plane, so just adjust the x to fit the distance between Test and the Z axis
    x = math.sqrt(y**2 + x**2)

    # initializing final tuple to return
    mangleRR= 0
    mangleRA= 0

    # equation k1 = k2*cos + k3*sin, came from circle equation from circle C
    k1 = x**2 + z**2 + (rR**2) - (rC**2)
    k2 = 2*x*rR
    k3 = 2*z*rR
    #print (f"k1: {k1} k2:{k2} k3: {k3}")

    try:
        if z > 0:
            # a*cos^2 + b*cos + c = 0
            a = -(k3**2)-(k2**2)
            b = 2*k1*k2
            c = k3**2-(k1**2)
            #print (f"a: {a} b: {b} c: {c}")

            quad = (-b + math.sqrt(b**2 - 4*a*c))/(2*a) # quadratic formula, get the lower right most solutiion
            mangleRR= np.arccos(quad)
        else:
            # a*sin^2 + b*sin + c = 0
            a = -(k2**2)-(k3**2)
            b = 2*k1*k3
            c = k2**2-(k1**2)

            quad = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)

            mangleRR = np.arcsin(quad)

    except ValueError:
        # print("math domain error")
        return "error"
    except ZeroDivisionError:
        # print("divide by zero")
        return "error"
    
    mangleRR = np.pi/2 - (mangleRR + csc.angle_RO_RR_RC) #90 degrees, getting the angle for the vertical piece in mainArm

    # just have to reverse it in here, because model thinks that CCW is positive
    csm.motorRR.angle = -mangleRR # after the angle is set, all the parent coordinate systems will update their points

    # make a couple of points dicts in csm, one updates parent with child (absolute), other updates child with parent (relative)
    distZ = z - csm["RC"].z
    distX = x - csm["RC"].x

    print("distZ: ", distZ)
    print("distX: ", distX)

    # angleD = math.atan2(distZ,distX) - csc.angle_HH_RA_RC #csc.angle_HH_RA_RC is local, need it to be global
    # angle_HH_RA_RC = math.atan((csm["RC"].z - csm["RA"].z)/(csm["RC"].x - csm["RA"].x))
    angle_HH_RA_RC = csm.motorRR.angle + csc.angle_HH_RA_RC
    angleD = math.atan2(distZ,distX) - angle_HH_RA_RC
    csm.motorRC.angle = angleD # setting this angle will update points CE and BC, and will propagate changes up the parent tree

    mangleRA = np.pi/2 - p.getAngleBetween(csm["AB"], csm["RA"], csm["RO"] )

    csm.motorRT.angle = angleRotation

    return (mangleRR, mangleRA)

# determines if test point is within circle C
def withinRange(test):
    return (csc.RC.magnitude() - csc.CE.magnitude() < test.distanceTo(csc.OO) and test.distanceTo(csc.OO) < csc.RC.magnitude() + csc.CE.magnitude())

# getting the proper step angle values for lineangleR0interpolation
def linearTravel(startPoint, endPoint, motorList, csm):

    # startPoint check the two points to see if they are reachable, do a within range
    returnString = "the following points are out of range: "
    if (not withinRange(startPoint)):
        returnString += str(startPoint)
    if (not withinRange(endPoint)):
        returnString += str(endPoint)

    # if returnString has changed, that means one of the points aren't within range
    if (len(returnString) != 39):
        print(returnString)
        return
    
    speed = smath.speed
    
    xLength = endPoint.x - startPoint.x
    yLength = endPoint.y - startPoint.y
    zLength = endPoint.z - startPoint.z
    totalLength = math.sqrt(xLength**2 + yLength**2 + zLength**2)
    totalTime = totalLength/speed

    # this is to set a minumum number of frames for the steps to work on, but with a smaller step size I don't think it is necessary
    if (totalTime/40 < smath.frameTime):
        smath.frameTime = totalTime/40

    frameSteps = math.ceil(totalTime/smath.frameTime)   # number of frames

    xFrame = xLength/frameSteps # caculating the distance each frame will go
    yFrame = yLength/frameSteps
    zFrame = zLength/frameSteps
    xIter = startPoint.x          # intializing the variables that will iterate
    yIter = startPoint.y
    zIter = startPoint.z
    test = p.Point(xIter, yIter, zIter)

    # need all 3 because of p2p where one dimension doesn't change but others do
    while (abs(xIter - startPoint.x) < abs(xLength) or abs(yIter - startPoint.y) < abs(yLength) or abs(zIter - startPoint.z < abs(zLength))):
        
        angles = findAngle2D(csm, test)
        for motor in motorList:
            motor.frameList.append(angles[motor.motorIndex])

        xIter += xFrame
        yIter += yFrame
        zIter += zFrame
        test = p.Point(xIter, yIter, zIter)
