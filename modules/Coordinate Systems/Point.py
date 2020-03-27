import numpy as np
import math

class Point:
    def __init__(self, x, y, z=0):
        self._homogeneous = np.array([x,y,z,1])
        self.x = x
        self.y = y
        self.z = z
        

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
        self.x = self._homogeneous[0]
        self.y = self._homogeneous[1]
        self.z = self._homogeneous[2]
        


class Circle(Point):
    def __init__(self, r, x, y, z=0):
        Point.__init__(self, x, y, z=0)
        self.radius = r

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

        return Point(x1+x2-x3, y1+y2-y3)

        # d = self.distanceTo(other)
        # print(d)
        # a = (self.radius**2 - other.radius**2 + d**2)/(2*d)
        # h = math.sqrt(self.radius**2 - a**2)
        # x2 = self.x + a*(other.x - self.x)/d
        # y2 = self.y + a*(other.y - self.y)/d
        # x3 = x2 - h*(other.x - self.x)/d
        # y3 = y2 - h*(other.y - self.y)/d

        # return Point(x3, y3)

BC = Circle(9.5, 4.50828, 2.59381)
RA = Circle(2.75, -2.4032, 3.18909)
AB = RA.intersectionPoint(BC)
print(AB)
print(RA)
print(BC)
print(AB.distanceTo(RA))
print(AB.distanceTo(BC))
