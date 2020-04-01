import numpy as np
import CoordinateSystem as cs
import math

class Point(object):
    def __init__(self, x, y, z=0):
        self._homogeneous = np.array([x,y,z,1])
        self._regular = self._homogeneous[:-1]
        self.x = x
        self.y = y
        self.z = z
        self.links = []
        self.state = "ready"

    def __getitem__(self, position):
        return self._homogeneous[position]

    def magnitude(self):
        return math.sqrt( self.x**2 + self.y**2 + self.z**2 )

    def distanceTo(self, otherPoint):
        distance = self.homogeneous[:-1] - otherPoint.homogeneous[:-1]
        return np.sqrt(np.einsum('i,i', distance, distance))
        # return math.sqrt((otherPoint.x - self.x)**2 +(otherPoint.y - self.y)**2 +(otherPoint.z - self.z)**2)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    @property
    def homogeneous(self):
        return self._homogeneous
    @homogeneous.setter
    def homogeneous(self, incomingArray):
        self._homogeneous = incomingArray
        self._regular = self._homogeneous[:-1]
        self.x = self._homogeneous[0]
        self.y = self._homogeneous[1]
        self.z = self._homogeneous[2]

        for link in self.links:
            self.state = "ready"
            link.update(self)

    @property
    def regular(self):
        return self._regular
    @regular.setter
    def regular(self, incomingArray):
        self._regular = incomingArray
        self._homogeneous = np.append(self.regular, 1 )
        self.x = self._regular[0]
        self.y = self._regular[1]
        self.z = self._regular[2]

        for link in self.links:
            link.update(self)
    

class Link(object):
    def __init__(self, length, pointA, pointB):
        self.length = length
        self.points = {}
        self.points[pointA] = pointB
        self.points[pointB] = pointA
        self.vector = pointB.regular - pointA.regular
        # self.pointA.links.append(self)
        # self.pointB.links.append(self)
        
        self.angle = 0

    def update(self, point):
        # find the location of the other point, based on distances
        if self.points[point].state == "nready":
            self.points[point].state = "waiting"
        elif self.points[point].state == "waiting":
            self.points[point].intersectionPoint() # need to put intersection
        elif self.points[point].state == "fixed":
            for link in self.points[point].links:
                if link != self: link.update()


    def findCommonPoint(self, link):
        list1 = self.points.values()
        list2 = link.points.values()
        return set(list1).intersection(list2).pop()

    def changeAngle(self, incomingAngle, baseLink):
        p = self.findCommonPoint(baseLink)
        r = getXYRotationMatrix(incomingAngle)
        notnormalized = np.dot(r, baseLink.vector)
        self.points[p].regular = self.points[p].regular*np.sqrt(notnormalized.dot(notnormalized))/np.sqrt(baseLink.vector.dot(baseLink.vector))


def getXYRotationMatrix(angle):

    a = np.array([[ np.cos(angle), -np.sin(angle),              0],
                  [ np.sin(angle),  np.cos(angle),              0],
                  [             0,              0,              1]])

    return a

class Circle(Point):
    def __init__(self, r, x, y, z=0):
        Point.__init__(self, x, y, z=0)
        self.radius = r

    # returns one of the intersection points between two circles
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

        return Point(x1+x2-x3, y1+y2-y3)

def getAngleBetween(a, pivot, b):
    return np.arccos(np.dot( a.homogeneous[:-1] - pivot.homogeneous[:-1], b.homogeneous[:-1] - pivot.homogeneous[:-1]) / (a.magnitude() * b.magnitude()) )



RA = Point(0,0)
AB = Point(0,2.75)
BC = Point(9.49669118,2.49928784)
RC = Point(9.43702304,0)
CE = Point(9.28188588, -6.49814839)
A = Link(2.75, RA, AB)
B = Link(9, AB, BC)
D = Link(11, BC, RC)
R = Link(9.7612, RA, RC)

print(A.findCommonPoint(B))
ABtest = (A.findCommonPoint(B))
print(ABtest.magnitude())