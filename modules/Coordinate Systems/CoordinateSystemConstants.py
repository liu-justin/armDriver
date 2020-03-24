import numpy as np
import math

class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.normalarray = np.array([x,y,z])
        self.nparray = np.array([x,y,z,1])
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def mag(self):
        return math.sqrt( self.x**2 + self.y**2 + self.z**2 )

def toPoint(x,y,z=0):
    return np.array([x,y,z,1])

def getTranslateMatrix(x,y,z):
    return np.array([[1,0,0,x],
                     [0,1,0,y],
                     [0,0,1,z],
                     [0,0,0,1]])

def getRotationMatrix(angleX, angleY, angleZ):
    a = np.array([[              1,               0,               0, 0],
                  [              0,  np.cos(angleX), -np.sin(angleX), 0],
                  [              0,  np.sin(angleX),  np.cos(angleX), 0],
                  [              0,               0,               0, 1]])

    b = np.array([[ np.cos(angleY),               0,  np.sin(angleY), 0],
                  [              0,               1,               0, 0],
                  [-np.sin(angleY),               0,  np.cos(angleY), 0],
                  [              0,               0,               0, 1]])

    c = np.array([[ np.cos(angleZ), -np.sin(angleZ),               0, 0],
                  [ np.sin(angleZ),  np.cos(angleZ),               0, 0],
                  [              0,               0,               1, 0],
                  [              0,               0,               0, 1]])

    return np.dot(c, np.dot(b, a))

lengthB = 9.5
lengthA = 2.75

# first coordinate system, motor RC ---------------------------------------------------------------

# points
CE = Point(6.5, 0)
BC = Point(-2.5, 0)

# matrix for children of this coordinate system, motor RC has no children

# second coordinate system, motor RR ------------------------------------------------------------------

# points
RO = Point(0, 2.5)
RA = Point(-2.40315424, 3.18909339)
RC = Point(6.99893387, 2.37783316)
OO = Point(0, 0)

angle_RO_RR_RC = np.arccos(np.dot(RO.normalarray, RC.normalarray)/(RO.mag()*RC.mag()))

# matrix for children of this coordinate system, only RC
angle_HH_RA_RC = np.tan(( RC.y - RA.y )/( RC.x - RA.x ))
A_RC_RR_1 = getRotationMatrix( 0, 0, angle_HH_RA_RC )
A_RC_RR_2 = getTranslateMatrix( RC.x, RC.y, RC.z )
A_RC_RR = np.dot( A_RC_RR_2, A_RC_RR_1 )

# third coordinate system, motor RT ----------------------------------------------------------------------

# points, motor RT has no additional points needed

# matrix for children of this coordinate system, only RR
A_RR_RT = getRotationMatrix( np.pi/2, 0, 0 )

