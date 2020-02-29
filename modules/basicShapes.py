import math
import numpy as np

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
        self.baseAngle = a

        # angle controls where the outside point is in the angulangleR0coordinate
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


# RR is at Point(0,0), RO is the middle point, RA is the back point, and RC is the front point, VT is the zero angle, straight up
class MainArm:
    def __init__(self):
        self._angle_VT_RR_RO = 0
        self.length_RR_RO = 2.5
        self.length_RO_RC = 7
        self.length_RO_RA = 2.5
        self.angle_RR_RO_RC = 89*2*np.pi/360
        self.angle_RR_RO_RA = (91+15)*np.pi/360
        self.length_RR_RC = math.sqrt(self.length_RR_RO**2 + self.length_RO_RC**2 - 2*self.length_RR_RO*self.length_RO_RC*math.cos(self.angle_RR_RO_RC))
        self.angle_RO_RR_RC = np.arcsin(math.sin(self.angle_RR_RO_RC)*self.length_RO_RC/self.length_RR_RC)
        self.length_RR_RA = math.sqrt(self.length_RR_RO**2 + self.length_RO_RA**2 - 2*self.length_RR_RO*self.length_RO_RA*math.cos(self.angle_RR_RO_RA))
        self.angle_RO_RR_RA = np.arcsin(math.sin(self.angle_RR_RO_RA)*self.length_RO_RA/self.length_RR_RA)

        self.RO = Point(self.length_RR_RO*math.sin(self.angle_VT_RR_RO),self.length_RR_RO*math.cos(self.angle_VT_RR_RO))
        self.point_RC_x = self.RO.x - self.length_RO_RC * math.sin(self.angle_RR_RO_RC-self.angle_VT_RR_RO)
        self.point_RC_y = self.RO.y - self.length_RO_RC * math.cos(self.angle_RR_RO_RC-self.angle_VT_RR_RO) #!!!
        self.RC = Point(self.point_RC_x, self.point_RC_y)
        self.point_RA_x = self.RO.x - self.length_RO_RA * math.sin(self.angle_RR_RO_RA+self.angle_VT_RR_RO)
        self.point_RA_y = self.RO.y - self.length_RO_RA * math.cos(self.angle_RR_RO_RA+self.angle_VT_RR_RO) #!!!        
        self.RA = Point(self.point_RA_x, self.point_RA_y)

    def refindPoints(self):
        self.RO = Point(self.length_RR_RO*math.sin(self.angle_VT_RR_RO),self.length_RR_RO*math.cos(self.angle_VT_RR_RO))
        self.point_RC_x = self.RO.x + self.length_RO_RC * math.sin(self.angle_RR_RO_RC-self.angle_VT_RR_RO)
        self.point_RC_y = self.RO.y - self.length_RO_RC * math.cos(self.angle_RR_RO_RC-self.angle_VT_RR_RO) #!!!
        self.RC = Point(self.point_RC_x, self.point_RC_y)
        self.point_RA_x = self.RO.x - self.length_RO_RA * math.sin(self.angle_RR_RO_RA-self.angle_VT_RR_RO)
        self.point_RA_y = self.RO.y + self.length_RO_RA * math.cos(self.angle_RR_RO_RA-self.angle_VT_RR_RO) #!!!        
        self.RA = Point(self.point_RA_x, self.point_RA_y)


    @property
    def angle_VT_RR_RO(self):
        return self._angle_VT_RR_RO

    @angle_VT_RR_RO.setter
    def angle_VT_RR_RO(self, a):
        self._angle_VT_RR_RO = a
        self.refindPoints()

ORIGIN = Point(0, 0)
linkR = Circle(ORIGIN, 7.39183102,0)
#linkR = Circle(ORIGIN, 6.92335156,0)
linkC = Circle(linkR.outside, 6.5,0)
MAINARM = MainArm()
print(MAINARM.length_RR_RC)