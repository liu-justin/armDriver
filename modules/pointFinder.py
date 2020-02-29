import math
import numpy as np
import time

import matplotlib.pyplot as plt
import modules.stepMath as smath

import modules.basicShapes as bs

# lengths of the 4angleR0linkage above the main arm
aLength = 2.75
bLength = 9.5
cLength = 2.5
dLength = 9.43702304

# find the angles of startPoint tilt and endPoint tilt motor
def findAngle2D(test, newzero=False):
    # renaming variables for the equation in the notebook
    x = test.x
    y = test.y # y is up
    z = test.z
    rR = bs.linkR.radius
    rC = bs.linkC.radius

    angleRotation = math.atan2(z,x)
    x = math.sqrt(z**2 + x**2)

    # initializing final tuple to return
    angleR0= 0
    angleRA= 0

    # equation k1 = k2*cos + k3*sin, came from circle equation from circle C
    k1 = x**2 + y**2 + (rR**2) - (rC**2)
    k2 = 2*x*rR
    k3 = 2*y*rR
    #print (f"k1: {k1} k2:{k2} k3: {k3}")

    try:
        if y > 0:
            # a*cos^2 + b*cos + c = 0
            a = -(k3**2)-(k2**2)
            b = 2*k1*k2
            c = k3**2-(k1**2)
            #print (f"a: {a} b: {b} c: {c}")

            quad = (-b + math.sqrt(b**2 - 4*a*c))/(2*a) # quadratic formula, get the lower right most solutiion
            #linkR.angle = np.arccos(quad)
            angleR0= np.arccos(quad)
        else:
            # a*sin^2 + b*sin + c = 0
            a = -(k2**2)-(k3**2)
            b = 2*k1*k3
            c = k2**2-(k1**2)

            quad = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)

            #linkR.angle = np.arcsin(quad)
            angleR0= np.arcsin(quad)

    except ValueError:
        print("math domain error")
    except ZeroDivisionError:
        print("divide by zero")
    
    # setting the angle on Circle R (necessary to get linkR.outside updated, so that linkC.center is updated)
    bs.linkR.angle = angleR0
    bs.linkC.baseAngle = angleR0

    # finding the angle on Circle C
    distY = y - bs.linkR.outside.y
    distX = x - bs.linkR.outside.x

    # this angle is referenced to the global reference plane, needs to be from angleR0angle reference plane
    # angleD is the angle inside the upper quad, so we have to reverse the angle
    angleD = angleR0- math.atan2(distY,distX)

    # geometry to get input stepper angle, using law of sines and cosines
    midLine = math.sqrt(cLength**2 + dLength**2 - 2*cLength*dLength*math.cos(angleD))
    angleCAD = np.arcsin(cLength*math.sin(angleD)/midLine)
    angleBAC = np.arccos((aLength**2 + midLine**2 - bLength**2)/(2*aLength*midLine))
    angleRA = angleCAD + angleBAC

    # not necessary when filling out angles from lineangleR0travel, only for drawing
    bs.linkC.angle = angleRA

    if (newzero):
        angleR0 = 90 - (angleR0 + bs.MAINARM.angle_RO_RR_RC)
        #angleRA = 90 - (angleRA + bs.MAINARM.angle_RO_RR_RA)
        return (angleR0, angleD)

    # adding missing radians(angle from base circle to RA to RC)
    angleRA += 0.1931807502

    # adding the missing radians from main amrs weird geometry (angle from base circle to R0 to RC)
    angleR0 += 1.243288929048

    return (angleR0, angleRA)

# looks like this is slower than what is already at line 148, uses a constraint equation
def findAngleRA(theta):
    start = time.perf_counter()    
    A = -2*aLength*dLength + 2*aLength*cLength*math.cos(theta)
    B = -2*aLength*cLength*math.sin(theta)
    C = aLength**2 - bLength**2 + cLength**2 + dLength**2 - 2*cLength*dLength*math.cos(theta)

    ending =  math.atan2(B,A) + np.arccos(-1*C/math.sqrt(A**2 + B**2))
    end = time.perf_counter()

    return ending, end-start


# determines if test point is within circle C
def withinRange(test):
    return (bs.linkR.radius - bs.linkC.radius < test.distanceTo(bs.ORIGIN) and test.distanceTo(bs.ORIGIN) < bs.linkR.radius + bs.linkC.radius)

# getting the proper step angle values for lineangleR0interpolation
def linearTravel(startPoint, endPoint, motorList):

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
    test = bs.Point(xIter, yIter, zIter)

    # just for the graph
    tIter = 0
    tList = []

    # need all 3 because of p2p where a dimension doesn't change but others do
    while (abs(xIter - startPoint.x) < abs(xLength) or abs(yIter - startPoint.y) < abs(yLength) or abs(zIter - startPoint.z < abs(zLength))):
        
        angles = findAngle2D(test)
        for motor in motorList:
            motor.frameList.append(angles[motor.motorIndex])

        xIter += xFrame
        yIter += yFrame
        zIter += zFrame
        test = bs.Point(xIter, yIter, zIter)

        # for the graph
        tList.append(tIter)
        tIter += smath.frameTime
    
    #--------------PLOTTING LINEAR POINT2POINT GRAPHS------------------
    fig, ax = plt.subplots()

    for motor in motorList:
        plt.plot(tList, motor.frameList, label=f"Motor {motor.motorIndex} frameList")
        #ax.scatter(tList, motor.frameList, s=4, label=f"{motor.motorIndex}")

    plt.xlabel("time (secs)")
    plt.ylabel("angle from east (radians)")
    minorTicks = np.arange(-np.pi, 1.5*np.pi, smath.stepAngle/2)
    #minorTicks = np.arange(1, 5, smath.stepAngle/2)
    ax.set_yticks(minorTicks, minor=True)
    plt.grid(b=True, which="minor")
    plt.legend()
  
    #--------------PLOTTING LINEangleR0POINT2POINT GRAPHS------------------
