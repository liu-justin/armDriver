import numpy as np
import CoordinateSystem as cs
import math

class Point(object):
    def __init__(self, name, x, y, z=0, state="nready"):
        self.name = name
        self._homogeneous = np.array([x,y,z,1])
        self._regular = self._homogeneous[:-1]
        self.x = x
        self.y = y
        self.z = z
        self.links = []
        self.waitingLinks = []
        self.state = state

    def __getitem__(self, position):
        return self._homogeneous[position]

    def magnitude(self):
        return math.sqrt( self.x**2 + self.y**2 + self.z**2 )

    def distanceTo(self, otherPoint):
        distance = self.regular - otherPoint.regular
        return np.sqrt(np.einsum('i,i', distance, distance))
        # return math.sqrt((otherPoint.x - self.x)**2 +(otherPoint.y - self.y)**2 +(otherPoint.z - self.z)**2)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def intersectionPoint(self):
        linkA = self.waitingLinks[0]
        linkB = self.waitingLinks[1]
        pointA = linkA.points[self]
        pointB = linkB.points[self]
        print(f"point {self.name} calculating intersection point between two links {linkA.name}, {linkB.name} - points are {pointA.name}:{pointA},{pointB.name}:{pointB}")
        x1 = 0.5*(pointA.x + pointB.x)
        y1 = 0.5*(pointA.y + pointB.y)

        R = pointA.distanceTo(pointB)

        c2 = (linkA.length**2 - linkB.length**2)/(2*R**2)
        x2 = c2*(pointB.x - pointA.x)
        y2 = c2*(pointB.y - pointA.y)

        c3_1 = 2*(linkA.length**2+linkB.length**2)/R**2
        c3_2 = (linkA.length**2-linkB.length**2)**2/R**4
        c3 = 0.5*math.sqrt(c3_1 - c3_2 - 1)
        x3 = c3*(pointB.y - pointA.y)
        y3 = c3*(pointA.x - pointB.x)

        self.waitingLinks = []

        return (x1+x2+x3, y1+y2+y3)

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
        self.state = "ready"
        for link in self.links: link.update(self)
            
            

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
        print(f"new regular for point {self.name}: {self}")

        self.state = "ready"

        print(f"going to update the following links: {[link.name for link in self.links]}")
        for link in self.links: link.update(self)
            
    

class Link(object):
    def __init__(self, name, length, pointA, pointB):
        self.name = name
        self.length = length
        self.points = {}
        self.points[pointA] = pointB
        self.points[pointB] = pointA
        self.vector = pointB.regular - pointA.regular
        pointA.links.append(self)
        pointB.links.append(self)
        
        self.angle = 0

    def update(self, point):
        # find the location of the other point, based on distances
        print(f"link {self.name} updating, currently updating point {self.points[point].name} ")
        if self.points[point].state == "nready":
            print("state was nready, so setting to waiting")
            self.points[point].state = "waiting"
            self.points[point].waitingLinks.append(self)

        # if another link put the point into waiting, that means it can be found thru intersection
        elif self.points[point].state == "waiting":
            print("state was waiting, so doing an intersection")
            self.points[point].waitingLinks.append(self)
            tup = self.points[point].intersectionPoint()
            # for link in self.points[point].waitingLinks: link.state = "ready"
            
            # cant use the property, because otherwise it would loop thru everything again
            # self.points[point]._regular = np.array([tup[0], tup[1], 0])
            # self.points[point].x = tup[0]
            # self.points[point].y = tup[1]
            self.points[point].regular = np.array([tup[0], tup[1], 0])

        # if the other point is fixed, search thru the other links from that point
        elif self.points[point].state == "fixed":
            print("state was fixed, so checking all the other links assoicated with this point")
            for link in self.points[point].links:
                if link != self: link.update(self.points[point])


    def findCommonPoint(self, link):
        list1 = self.points.values()
        list2 = link.points.values()
        return set(list1).intersection(list2).pop()

    def changeAngle(self, incomingAngle, baseLink):
        p = self.findCommonPoint(baseLink)
        print(f"finding common point for {self.name}, {baseLink.name}: {p.name}")
        r = getXYRotationMatrix(incomingAngle)
        notnormalized = np.dot(r, baseLink.vector)
# this is not right, need to add the first point position
        self.points[p].regular = notnormalized*np.sqrt(self.vector.dot(self.vector))/np.sqrt(baseLink.vector.dot(baseLink.vector))

def getXYRotationMatrix(angle):

    a = np.array([[ np.cos(angle), -np.sin(angle),              0],
                  [ np.sin(angle),  np.cos(angle),              0],
                  [             0,              0,              1]])

    return a

# class Circle(Point):
#     def __init__(self, r, x, y, z=0):
#         Point.__init__(self, x, y, z=0)
#         self.radius = r

#     # returns one of the intersection points between two circles
#     def intersectionPoint(self, other):
#         x1 = 0.5*(self.x + other.x)
#         y1 = 0.5*(self.y + other.y)

#         R = self.distanceTo(other)

#         c2 = (self.radius**2 - other.radius**2)/(2*R**2)
#         x2 = c2*(other.x - self.x)
#         y2 = c2*(other.y - self.y)

#         c3_1 = 2*(self.radius**2+other.radius**2)/R**2
#         c3_2 = (self.radius**2-other.radius**2)**2/R**4
#         c3 = 0.5*math.sqrt(c3_1 - c3_2 - 1)
#         x3 = c3*(other.y - self.y)
#         y3 = c3*(self.x - other.x)

#         return Point(x1+x2-x3, y1+y2-y3)

def getAngleBetween(a, pivot, b):
    return np.arccos(np.dot( a.homogeneous[:-1] - pivot.homogeneous[:-1], b.homogeneous[:-1] - pivot.homogeneous[:-1]) / (a.magnitude() * b.magnitude()) )
