import math
import numpy as np
import turtle
import time

import matplotlib.pyplot as plt
import modules.stepMath as smath

class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def distanceTo(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Circle(Point):
    def __init__(self, point, r, a):
        self.center = point
        self.radius = r

        # angle for _angle to reference off of (2nd tilt motor is referenced off of 1st tilt motor angle)
        self.base_angle = a

        # angle controls where the outside point is in the angular coordinate
        self._angle = a

        # outside point will sit on the circle circumference, always radius length away from center point
        self.outside = Point(self.x + r*math.cos(self.angle),self.y + r*math.sin(self.angle))
    
    # returns one of the intersection points between two circles, obsolete i think
    def intersectionPoint(self, other):
        x1 = 0.5*(self.x + other.x)
        y1 = 0.5*(self.y + other.y)

        R = self.distanceTo(other)

        c2 = (self.radius**2 - other.radius**2)/(2*R**2)
        x2 = c2*(other.x - self.x)
        y2 = c2*(other.y - self.y)

        c3_1 = 2*(self.radius**2+other.radius**2)/R**2
        c3_2 = (self.radius**2-other.radius**2)**2/R**4
        c3 = 0.5*math.sqrt(c3_1 - c3_2 - 1)
        x3 = c3*(other.y - self.y)
        y3 = c3*(self.x - other.x)

        return Point(x1+x2+x3, y1+y2+y3)        

    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, a):
        self._angle = a
        self.outside.x = self.x + self.radius*math.cos(self._angle)
        self.outside.y = self.y + self.radius*math.sin(self._angle)

    @property
    def x(self):
        return self.center.x       
    @x.setter
    def x(self, x):
        self.center.x = x
        self.outside.x = self.x + self.radius*math.cos(self._angle)

    @property
    def y(self):
        return self.center.y    
    @y.setter
    def y(self, y):
        self.center.y = y
        self.outside.y = self.y + self.radius*math.sin(self._angle)

ORIGIN = Point(0, 0)
linkR = Circle(ORIGIN, 7.39183102,0)
linkC = Circle(linkR.outside, 6.5,0)

# lengths of the 4bar linkage above the main arm
aLength = 2.75
bLength = 9.5
cLength = 2.5
dLength = 9.43702304

# find the angles of startPoint tilt and endPoint tilt motor
def findAngle2D(test):
    # renaming variables for the equation in the notebook
    x = test.x
    y = test.y
    rR = linkR.radius
    rC = linkC.radius

    # initializing final tuple to return
    aR = 0
    aC = 0

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
            aR = np.arccos(quad)
        else:
            # a*sin^2 + b*sin + c = 0
            a = -(k2**2)-(k3**2)
            b = 2*k1*k3
            c = k2**2-(k1**2)

            quad = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)

            #linkR.angle = np.arcsin(quad)
            aR = np.arcsin(quad)

    except ValueError:
        print("math domain error")
    except ZeroDivisionError:
        print("divide by zero")

    # setting the angle on Circle R (necessary to get linkR.outside updated, so that linkC.center is updated)
    linkR.angle = aR

    # finding the angle on Circle C
    distY = y - linkR.outside.y
    distX = x - linkR.outside.x

    # this angle is referenced to the global reference plane, needs to be from aR angle reference plane
    # angleD is the angle inside the upper quad, so we have to reverse the angle
    angleD = aR - math.atan2(distY,distX)

    # geometry to get input stepper angle 
    start = time.perf_counter()
    midLine = math.sqrt(cLength**2 + dLength**2 - 2*cLength*dLength*math.cos(angleD))
    angleCAD = np.arcsin(cLength*math.sin(angleD)/midLine)
    angleBAC = np.arccos((aLength**2 + midLine**2 - bLength**2)/(2*aLength*midLine))
    end = time.perf_counter()

    aC = angleCAD + angleBAC
    print(f"ac: {aC}, time: {end-start}")
    aC2 = findAngleRA(angleD)
    print(f"ac2: {aC2[0]}, time: {aC2[1]}")


    # not necessary when filling out angles from linear travel, only for drawing
    linkC.angle = aC

    return (aR, aC)

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
    return (linkR.radius - linkC.radius < test.distanceTo(ORIGIN) and test.distanceTo(ORIGIN) < linkR.radius + linkC.radius)

# getting the proper step angle values for linear interpolation
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
    totalLength = math.sqrt(xLength**2 + yLength**2)
    totalTime = totalLength/speed

    # frames set the angle coordinates for linear interpolation 
    if (totalTime/40 < smath.frameTime):
        smath.frameTime = totalTime/40

    frameSteps = math.ceil(totalTime/smath.frameTime)   
    xFrame = xLength/frameSteps
    yFrame = yLength/frameSteps
    xIter = startPoint.x
    yIter = startPoint.y
    test = Point(xIter, yIter)

    # just for the graph
    tIter = 0
    tList = []

    while (abs(xIter - startPoint.x) < abs(xLength) or abs(yIter - startPoint.y) < abs(yLength)):
        
        angles = findAngle2D(test)
        for motor in motorList:
            motor.frameList.append(angles[motor.motorIndex])

        xIter += xFrame
        yIter += yFrame
        test = Point(xIter, yIter)

        # for the graph
        tList.append(tIter)
        tIter += smath.frameTime
    
    #--------------PLOTTING LINEAR POINT2POINT GRAPHS------------------
    # fig, ax = plt.subplots()

    # for motor in motorList:
    #     #ax.plot(tList, motor.frameList, label=f"{motor.motorIndex}")
    #     ax.scatter(tList, motor.frameList, s=4, label=f"{motor.motorIndex}")

    # plt.xlabel("time (secs)")
    # plt.ylabel("angle from east (radians)")
    # minorTicks = np.arange(-np.pi, np.pi, smath.stepAngle)
    # ax.set_yticks(minorTicks, minor=True)
    # plt.grid(b=True, which="minor")
    # plt.legend()
    # #plt.show()
    #--------------PLOTTING LINEAR POINT2POINT GRAPHS------------------




class MyTurtle(turtle.Turtle):
     
    def __init__(self):
        """Turtle Constructor"""
        turtle.Turtle.__init__(self, shape="turtle")
 
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
            test = Point(i,j)
            angle = findAngle(test)

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

# uses findAngle and draws the correct links to the point
def singlePoint(x,y):
    test = Point(x, y)

    print(linkC.outside.distanceTo(linkC.center))
    
    testArc = Circle(ORIGIN,test.distanceTo(ORIGIN), 0)

    angles = findAngle(test)
    linkR.angle = angles[0]
    linkC.angle = angles[1]
    #linkC.angle = -test.angle
    print(f"angles: {angles[0]}, {angles[1]}")


    t = MyTurtle()
    t.speed(0)
    t.hideturtle()

    t.drawCircle(linkR, "black")
    t.drawCircle(linkC, "black")
    t.drawCircle(testArc, "red")
    t.drawCross(ORIGIN, "black")
    t.drawCross(linkC.outside, "black")
    t.drawCross(linkC.center, "black")
    t.drawCross(test, "red")
    #t.drawCross(testArc.intersectionPoint(linkC))

    turtle.getscreen()._root.mainloop()

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

    turtle.getscreen()._root.mainloop()

