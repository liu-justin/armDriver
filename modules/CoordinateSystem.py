import numpy as np
import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# each child can only have one parent, so should each coordinate system have a matrix to get to the parent coordinateSystem
# - no, because the coordinate system has no idea how to get to the parent coordinateSystem without the parents points
# alternative is passing in the matrix with the coordinateSystem in args

class coordinateSystem(object):
    def __init__(self):
        self.points = {}
        self._angle = 0
        # z will always be the axis for rotation
        self.rotationMatrix = getRotationMatrix(0,0,self._angle)
        # self.children = args # [tuple(coordinateSystem, matrix)]

    def addPoint(self, key, x, y=0, z=0):
        self.points[key] = np.array([x, y, z, 1])

    def rotatePointsTo(self, angle):
        self.angle = angle
        # self.points = {p:np.dot(self.rotationMatrix, self.points[p]) for p in self.points}
        self.points = {k:np.dot(self.rotationMatrix, v) for k,v in self.points.items()}

    def updatePoints(self, prevCS, matrix):
        # transform the points first, using transform and rotation to get from this coordinate system to the nextCS
        newPoints = {k:np.dot(matrix, v) for k,v in prevCS.points.items()}

        # then transfer the points
        self.points.update(newPoints)

    def plotAllPoints(self, ax):
        for k,v in self.points.items():
            ax.scatter3D(v[0], v[1], v[2])
            ax.text(v[0], v[1], v[2], k)

    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, a):
        self._angle = a
        # this reassignment has around the same runtime as reassigning each entry individually
        self.rotationMatrix = getRotationMatrix(0,0,self._angle)

class coordinateSystemManager(coordinateSystem):
    def __init__(self):
        self.coordinateSystemDict = {}

    def addCoordinateSystem(self,key):
        self.coordinateSystemDict[key] = coordinateSystem()

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

# declaring all coordinate systems
motorRC = coordinateSystem()
motorRR = coordinateSystem()
motorRT = coordinateSystem()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# first coordinate system --------------------------------

motorRC.addPoint('CE', 6, 0) # add points to the coordinate system
motorRC.addPoint('BC', -2, 0)

# second coordinate system ---------------------------------

motorRR.addPoint('RO', 0, 2.5)
motorRR.addPoint('RA', -2.40315424, 3.18909339)
motorRR.addPoint('RC', 6.99893387, 2.37783316) # add points to the coordinate system
motorRR.addPoint('OO', 0, 0)

angle_HH_RA_RC = np.tan((motorRR.points['RC'][1]-motorRR.points['RA'][1])/(motorRR.points['RC'][0]-motorRR.points['RA'][0]))
A_RC_RR_1= getRotationMatrix(0,0,angle_HH_RA_RC)
A_RC_RR_2 = getTranslateMatrix(motorRR.points['RC'][0], motorRR.points['RC'][1], motorRR.points['RC'][2])
A_RC_RR = np.dot(A_RC_RR_2, A_RC_RR_1) # get the transformation matrix from coordinate system RC to RR

# third coordinate system ---------------------------------
A_RR_RT = getRotationMatrix(np.pi/2, 0, 0)

# changing motor angles-----------------------------------------
motorRC.rotatePointsTo(-np.pi/4)

motorRR.updatePoints(motorRC, A_RC_RR) # bring in points from coordinate system RC
motorRR.rotatePointsTo(np.pi/-6) # rotate all the points in RC

motorRT.updatePoints(motorRR, A_RR_RT)
motorRT.rotatePointsTo(np.pi/3)

# plotting --------------------------------------------------

motorRT.plotAllPoints(ax)

ax.set_xlabel('X (in)')
ax.set_ylabel('Y (in)')
ax.set_zlabel('Z (in)')

ax.set_xlim3d(-15, 15)
ax.set_ylim3d(-15, 15)
ax.set_zlim3d(-15, 15)

plt.show()