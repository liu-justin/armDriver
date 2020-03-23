# import modules.basicShapes as bs
# import modules.weightManager as wm
import CoordinateSystem as cs
import turtle
import math
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ORIGIN = bs.ORIGIN
linkR = bs.linkR
linkC = bs.linkC

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

            mangleRR= np.arcsin(quad)

    except ValueError:
        # print("math domain error")
        return "error"
    except ZeroDivisionError:
        # print("divide by zero")
        return "error"
    
    mangleRR = np.pi/2 - (mangleRR + bs.MAINARM.angle_RO_RR_RC) #90 degrees, getting the angle for the vertical piece in mainArm

    # setting the mangle for mainarm and getting all of the subsequent variables of mainarm
    bs.MAINARM.angle_VT_RR_RO = mangleRR

    distY = y - bs.MAINARM.RC.y
    distX = x - bs.MAINARM.RC.x
    #tempVector = np.array([distX, distY])

    # this angle is referenced to the global reference plane, needs to be from mangleRRangle reference plane
    # angleD is the angle inside the upper quad, so we have to reverse the angle
    angleD = math.atan2(distY,distX) - bs.MAINARM.vangle_RA_RC
    bs.linkC.center = bs.MAINARM.RC
    bs.linkC.refAngle = bs.MAINARM.vangle_RA_RC
    bs.linkC.angle = angleD # setting the angle finds outside again, so make sure to do it last
    
    # geometry to get input stepper angle, using law of sines and cosines
    midLine = math.sqrt(cLength**2 + dLength**2 - 2*cLength*dLength*math.cos(angleD))
    angleCAD = np.arcsin(cLength*math.sin(angleD)/midLine)
    angleBAC = np.arccos((aLength**2 + midLine**2 - bLength**2)/(2*aLength*midLine))
    mangleRA = angleCAD + angleBAC

    return (mangleRR, mangleRA)