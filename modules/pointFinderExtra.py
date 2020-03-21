import modules.basicShapes as bs
import modules.pointFinder as p
import modules.weightManager as wm
import turtle
import math
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ORIGIN = bs.ORIGIN
linkR = bs.linkR
linkC = bs.linkC

class MyTurtle(turtle.Turtle):
     
    def __init__(self):
        """Turtle Constructor"""
        turtle.Turtle.__init__(self, shape="turtle")

    def pointPosition(self, point):
        self.setposition(point.x*10,point.y*10)
 
    #Moves the turtle to the correct position and draws a circle    
    def drawCircle(self, circle, color="black"):
        

        self.color(color)
        self.penup()

        # drawing line from center to outside
        self.setposition(circle.x*10, circle.y*10)
        self.pendown()
        self.setposition(circle.outside.x*10, circle.outside.y*10)
        self.penup()

        # drawing circle
        self.setposition(circle.x*10, 10*(circle.y - circle.radius))
        self.pendown()
        self.setheading(0)
        self.circle(circle.radius*10)

    # draws a cross at the correct location
    def drawCross(self, other, color="black"):
        self.color(color)
        self.penup()
        self.setposition(other.x*10, 10*other.y)
        self.setheading(0)
        self.pendown()
        self.forward(2)
        self.backward(4)
        self.setposition(other.x*10, other.y*10)
        self.setheading(90)
        self.forward(2)
        self.backward(4)
        self.penup()

        # set up for drawing text next to the cross
        self.setposition(other.x*10+6, other.y*10-5)

    def drawMainArm(self, main, color="black"):
        self.color(color)
        self.penup()
        self.pointPosition(bs.ORIGIN)
        self.pendown()
        self.pointPosition(main.RO)
        self.pointPosition(main.RC)
        self.penup()
        self.pointPosition(main.RO)
        self.pendown()
        self.pointPosition(main.RA)
        self.penup()


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
            #linkR.angle = np.arccos(quad)
            mangleRR= np.arccos(quad)
        else:
            # a*sin^2 + b*sin + c = 0
            a = -(k2**2)-(k3**2)
            b = 2*k1*k3
            c = k2**2-(k1**2)

            quad = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)

            #linkR.angle = np.arcsin(quad)
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
    # bs.linkC.center = bs.MAINARM.RC
    # bs.linkC.refAngle = bs.MAINARM.vangle_RA_RC
    bs.linkC.angle = angleD # setting the angle finds outside again, so make sure to do it last
    # print(bs.linkC)
    

    # geometry to get input stepper angle, using law of sines and cosines
    # midLine = math.sqrt(cLength**2 + dLength**2 - 2*cLength*dLength*math.cos(angleD))
    # angleCAD = np.arcsin(cLength*math.sin(angleD)/midLine)
    # angleBAC = np.arccos((aLength**2 + midLine**2 - bLength**2)/(2*aLength*midLine))
    # mangleRA = angleCAD + angleBAC

    return (mangleRR, angleD)


# uses findAngle and draws the correct links to the point
def singlePoint(test):

    weighter = wm.WeightManager()
    
    angles = findAngle2D(test, True)
    weighter.appendPoint(bs.MAINARM.RA, 36.4) # 36.4 oz is weight of a NEMA23
    print(f"total torque in ozin: {weighter.calcTorque()}")
    # linkC = bs.Circle(bs.MAINARM.RC, 6.5, bs.MAINARM.vangle_RA_RC)
    # linkC.angle = angles[1]
    # print(linkC)
    print(f"angles: {angles[0]}, {angles[1]}")

    print(f"linkC outside point: {bs.linkC.outside}")

    t = MyTurtle()
    t.speed(0)
    t.hideturtle()
    t.drawMainArm(bs.MAINARM)
    t.drawCircle(bs.linkC, "black")
    t.drawCross(ORIGIN, "black")
    t.drawCross(test, "red")

    t.getscreen()._root.mainloop()

# shows the range of the machine
def multiplePoint():
    
    # initialize turtle
    t = MyTurtle()
    t.speed(0)
    t.hideturtle()

    t.drawCircle(linkR, "black")
    t.drawCross(ORIGIN, "black")

    # iterate through a grid of points, black points are reachable and grey points are not
    for i in range(0,13):
        for j in range(-12,12):
            test = bs.Point(i,j)
            angle = p.findAngle2D(test, True)

            # if the linkC overlaps directly ontop of test
            if (abs(linkR.outside.distanceTo(test)-6.5) <=0.0001):
                t.drawCross(test, "black")
                #t.write(linkR.angle *360/(2*np.pi))  # prints the angle number next to the cross, only use when i is limited to 1 increment
                #linkT = Circle(linkR.outside.x,linkR.outside.y,6.5,0) # initialize and draw the circle to see movement
                #t.drawCircle(linkT,"grey")

            # if linkC doesn't overlap with test
            else:
                t.drawCross(test, "red")
                # linkR.angle = linkR.angle + np.pi/4 # I dunno what this is, so I just comment it out
                # t.write(linkR.angle * 360/(2*np.pi)) # prints the angle number

    t.getscreen()._root.mainloop()

# shows the torque about RR at each of the test Points available
def torquePointPlot():
    w = wm.WeightManager()
    # iterate through a grid of points, black points are reachable and grey points are not
    for i in range(0,26):
        for j in range(-26,26):
            w.clear()

            test = bs.Point(i/2,j/2)
            angles = findAngle2D(test, True)
            if angles == "error":
                continue

            bs.MAINARM.angle_VT_RR_RO = angles[0]
            w.appendPoint(bs.MAINARM.RA, 36.4) # 36.4 oz is weight of a NEMA23
            w.appendTorquePlot(i,j)

    xPlot = np.array([i[0] for i in w.torquePlot])
    yPlot = np.array([i[1] for i in w.torquePlot])
    tqPlot = np.array([i[2] for i in w.torquePlot])

    fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(xPlot, yPlot, tqPlot)

    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xPlot, yPlot, tqPlot)

    ax.set_xlabel('X (in)')
    ax.set_ylabel('Y (in)')
    ax.set_zlabel('Torque about RR (oz-in)')

    plt.show()

def adjustmentsPlot(param): # no need for kwargs here, because we can only have one args
    # getattr(bs.MAINARM, param)
    middle = bs.MAINARM.d[param]
    
    rangeParam = np.arange(middle*0.5, middle*1.5, middle*0.1)

    adjustmentList = [] # list of tuples, (param, max)

    w = wm.WeightManager()
    # iterate through a grid of points, black points are reachable and grey points are not
    for p in rangeParam:
        bs.MAINARM.d[param] = p
        w.clearTorquePlot()
        for i in range(0,13):
            for j in range(-13,13):
                w.clear()

                test = bs.Point(i,j)
                angles = findAngle2D(test, True)
                if angles == "error":
                    continue

                bs.MAINARM.angle_VT_RR_RO = angles[0]
                w.appendPoint(bs.MAINARM.RA, 36.4) # 36.4 oz is weight of a NEMA23
                w.appendTorquePlot(i,j)
        tqArray = np.array([a[2] for a in w.torquePlot])
        tqMax = np.max(tqArray)
        tqMin = np.min(tqArray)

        adjustmentList.append((p, max(tqMax, tqMin)))

    fig = plt.figure()
    plt.plot([i[0] for i in adjustmentList], [i[1] for i in adjustmentList])
    plt.xlabel(param)
    plt.ylabel("Torque (ozin)")
    plt.show()


# draws the path of the point in turtle
def drawAngleList(motorList):
    t = MyTurtle()
    t.speed(0)
    t.hideturtle()

    t.drawCircle(linkR, "black")
    t.drawCross(ORIGIN, "black")

    for i in motorList:
        # x = linkR.radius * math.cos(i[0]) + linkC.radius * math.cos(i[1])
        # y = linkR.radius * math.sin(i[0]) + linkC.radius * math.sin(i[1])
        linkR.angle = i[0]
        linkC.angle = i[1]

        #t.drawCircle(linkC)
        t.drawCross(linkC.outside)

    t.getscreen()._root.mainloop()
