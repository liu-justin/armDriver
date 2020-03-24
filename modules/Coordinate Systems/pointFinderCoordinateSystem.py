# import modules.basicShapes as bs
# import modules.weightManager as wm
import CoordinateSystemConstants as csc
import turtle
import math
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ORIGIN = bs.ORIGIN
linkR = bs.linkR
linkC = bs.linkC

def findAngle2D(test, csm):
    # renaming variables for the equation in the notebook
    x = test.x
    y = test.y # y is up
    z = test.z
    rR = math.sqrt(csc.RC.x**2 + csc.RC.y**2)
    rC = math.sqrt(csc.CE.x**2 + csc.CE.y**2)

    angleRotation = math.atan2(z,x)
    x = math.sqrt(z**2 + x**2)

    # initializing final tuple to return
    mangleRR= 0
    mangleRA= 0

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
    csm.motorRR.angle = -mangleRR
    # just used the last matrix RT because it catches all the changes to angles
    csm.motorRT.update()

    # make a couple of points dicts in csm, one updates parent with child (absolute), other updates child with parent (relative)
    distY = y - csm.RR.points["RC"][1]
    distX = x - csm.RR.points["RC"][0]
    # distY = y - bs.MAINARM.RC.y
    # distX = x - bs.MAINARM.RC.x
    #tempVector = np.array([distX, distY])

    angleD = math.atan2(distY,distX) - csc.angle_HH_RA_RC
    csm.motorRC.angle = angleD # setting the angle finds outside again, so make sure to do it last
    csm.motorRT.update() # fixes all the angles for all the coordinate systems


    # want to replace this with something else in csm
    aLength = 2.75
    bLength = 9.5
    cLength = 2.5
    dLength = 9.43702304
    
    # geometry to get input stepper angle, using law of sines and cosines
    midLine = math.sqrt(cLength**2 + dLength**2 - 2*cLength*dLength*math.cos(angleD))
    angleCAD = np.arcsin(cLength*math.sin(angleD)/midLine)
    angleBAC = np.arccos((aLength**2 + midLine**2 - bLength**2)/(2*aLength*midLine))
    mangleRA = angleCAD + angleBAC

    return (mangleRR, mangleRA)