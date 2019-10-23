import math
import numpy as np
import turtle

import matplotlib.pyplot as plt
import pandas


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def distance_to(self, other):
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
    
    # returns one of the intersection points between two circles,
    def intersectionPoint(self, other):
        x1 = 0.5*(self.x + other.x)
        y1 = 0.5*(self.y + other.y)

        R = self.distance_to(other)

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

# dont think I used this at all, determines if test point is within circle C
def withinRange(R, C, test):
    return (R.radius - C.radius < test.distance_to(ORIGIN) and test.distance_to(ORIGIN) < R.radius + C.radius)

# find the angles of first tilt and second tilt motor
def findAngle(test):
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
            # a*sin^2 + b*sin + c = 0
            a = -(k3**2)-(k2**2)
            b = 2*k1*k2
            c = k3**2-(k1**2)

            #print (f"a: {a} b: {b} c: {c}")

            # quadratic formula, guess and checked to get the lower right most solutiion
            quad = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
            #linkR.angle = np.arccos(quad)
            aR = np.arccos(quad)
        else:
            # a*cos^2 + b*cos + c = 0
            a = -(k2**2)-(k3**2)
            b = 2*k1*k3
            c = k2**2-(k1**2)

            #print (f"a: {a} b: {b} c: {c}")
            #print(f"a: {a} b: {b} c: {c} determinant: {b**2 - 4*a*c}")
            quad = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)

            #linkR.angle = np.arcsin(quad)
            aR = np.arcsin(quad)

    except ValueError:
        print("math domain error")
    except ZeroDivisionError:
        print("divide by zero")

    # setting the angle on Circle R ( necessary to get linkR.outside updated, so that linkC.center is updated)
    linkR.angle = aR

    # finding the angle on Circle C
    distY = y - linkR.outside.y
    distX = x - linkR.outside.x

    aC = math.atan2(distY,distX)

    # not necessary when only filling out angles from linear travel, but necessary otherwise
    linkC.angle = aC

    #print(f"{aR} {aC}")

    return (aR, aC)

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
            if (abs(linkR.outside.distance_to(test)-6.5) <=0.0001):
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

    print(linkC.outside.distance_to(linkC.center))
    
    testArc = Circle(ORIGIN,test.distance_to(ORIGIN), 0)

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

def nearestStep(value, step):
    if value%step < step/2:
        return value//step*step
    else:
        return (value//step + 1)*step

# rounds every point to the nearest step
def linearTravel(first, second):

    # first check the two points to see if they are reachable, do a within range
    returnString = "the following points are out of range: "
    if (not withinRange(linkR, linkC,first)):
        returnString += str(first)
    if (not withinRange(linkR, linkC,second)):
        returnString += str(second)

    # if returnString has changed, that means one of the points aren't within range
    if (len(returnString) != 39):
        print(returnString)
        return
    
    speed = 4 # in/s
    
    xLength = second.x - first.x
    yLength = second.y - first.y
    totalLength = math.sqrt(xLength**2 + yLength**2)

    totalTime = totalLength/speed
    print(f"total time: {totalTime}")

    # I just guess and checked on the graph, and this value is the highest that gave a smooth curve
    frameTime = 0.01

    singleStepAngle = (1.8 *np.pi/180)

    # if the distance is super small, and the total time is less than frame time
    if (totalTime < frameTime*2):
        frameTime = totalTime/2

    # just for the graph
    tIter = 0
    tList = []

    frameSteps = math.ceil(totalTime/frameTime)   
    xFrame = xLength/frameSteps
    yFrame = yLength/frameSteps

    xIter = first.x
    yIter = first.y
    test = Point(xIter, yIter)

    angleList = []
    angleStepList = []

    while (abs(xIter - first.x) < abs(xLength) or abs(yIter - first.y) < abs(yLength)):
        
        angles = findAngle(test)
        angleList.append(angles)
        nearestR = nearestStep(angles[0], singleStepAngle)
        nearestC = nearestStep(angles[1], singleStepAngle)
        angleStepList.append((nearestR, nearestC))
        #angleList.append((xIter, yIter))

        # for the graph
        tList.append(tIter)

        xIter += xFrame
        yIter += yFrame
        test = Point(xIter, yIter)

        tIter += frameTime
    
    # plotting both angles
    tArray = np.asarray(tList, dtype=np.float32)
    angleRArray = np.asarray([elem[0] for elem in angleList])
    angleCArray = np.asarray([elem[1] for elem in angleList])
    angleRStep = np.asarray([elem[0] for elem in angleStepList])
    angleCStep = np.asarray([elem[1] for elem in angleStepList])

    fig, ax = plt.subplots()

    ax.plot(tArray, angleRArray, label="angleR")
    ax.scatter(tArray, angleRStep, s=4, label="angleR frames")
    ax.plot(tArray, angleCArray, label="angleC")
    ax.scatter(tArray, angleCStep, s=4, label="angleC frames")
    plt.xlabel("time (secs)")
    plt.ylabel("angle from east (radians)")
    plt.legend()
    #plt.show()  

    return angleStepList

def drawAngleList(angles):
    t = MyTurtle()
    t.speed(0)
    t.hideturtle()

    t.drawCircle(linkR, "black")
    t.drawCross(ORIGIN, "black")

    for i in angles:
        # x = linkR.radius * math.cos(i[0]) + linkC.radius * math.cos(i[1])
        # y = linkR.radius * math.sin(i[0]) + linkC.radius * math.sin(i[1])
        linkR.angle = i[0]
        linkC.angle = i[1]

        #t.drawCircle(linkC)
        t.drawCross(linkC.outside)

    turtle.getscreen()._root.mainloop()

