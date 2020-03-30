# import modules.basicShapes as bs
# import modules.weightManager as wm
import CoordinateSystemConstants as csc
import Point as p
import turtle
import math
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def findAngle2D(csm, x, y, z=0):
    # # renaming variables for the equation in the notebook
    # x = test.x
    # y = test.y # y is up
    # z = test.z
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
    csm.motorRR.angle = -mangleRR # after the angle is set, all the parent coordinate systems will update their points

    # make a couple of points dicts in csm, one updates parent with child (absolute), other updates child with parent (relative)
    distY = y - csm["RC"].y
    distX = x - csm["RC"].x

    print("distY: ", distY)
    print("distX: ", distX)

    angleD = math.atan2(distY,distX) - csc.angle_HH_RA_RC
    csm.motorRC.angle = -angleD # setting this angle will update points CE and BC, and will propagate changes up the parent tree

    mangleRA = np.pi/2 - p.getAngleBetween(csm["AB"], csm["RA"], csm["RO"] )

    return (mangleRR, mangleRA)