import numpy as np
import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class coordinateSystem(object):
    def __init__(self):
        self.points = {}
        self._angle = 0
        # z will always be the axis for rotation
        self.rotationMatrix = getXYRotationMatrix(self._angle)

    def addPoint(self, key, point):
        self.points[key] = point

    def rotatePoints(self):
        # self.points = {p:np.dot(self.rotationMatrix, self.points[p]) for p in self.points}
        self.points = {k:np.dot(self.rotationMatrix, v) for k,v in self.points.items()}

    def updatePoints(self, prevCS, matrix):
        # transform the points first, using transform and rotation to get from this coordinate system to the nextCS
        prevCS.points = {k:np.dot(matrix, v) for k,v in prevCS.points.items()}

        # then transfer the points
        self.points.update(prevCS.points)

    def plotAllPoints(self, ax):
        for k,v in self.points.items():
            ax.scatter3D(v[0], v[1], v[2])
# ax.plot3D(list(motorRR.points.values())[:,0], list(motorRR.points.values())[:,1], list(motorRR.points.values())[:,2])

    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, a):
        self._angle = a
        # this reassignment has around the same runtime as reassigning each entry individually
        self.rotationMatrix = getXYRotationMatrix(self._angle)

def getTranslateMatrix(x,y,z):
    return np.array([[1,0,0,x],
                     [0,1,0,y],
                     [0,0,1,z],
                     [0,0,0,1]])

def getXYRotationMatrix(angle):
    return np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                     [np.sin(angle),  np.cos(angle), 0, 0],
                     [            0,              0, 1, 0],
                     [            0,              0, 0, 1]])

# declaring all coordinate systems
motorRC = coordinateSystem()
motorRR = coordinateSystem()
motorRT = coordinateSystem()

# first coordinate system

CE = np.array([0,6,0,1])
motorRC.addPoint('CE', CE) # add points to the coordinate system

motorRC.angle = -np.pi/4 # rotate all the points; can maybe squish these two together, this and the line below
motorRC.rotatePoints()

# second coordinate system

RO = np.array([0, 2.5, 0, 1])
RA = np.array([-2.40315424, 3.18909339, 0, 1])
RC = np.array([6.99893387, 2.37783316, 0, 1])
motorRR.addPoint('RO', RO)
motorRR.addPoint('RA', RA)
motorRR.addPoint('RC', RC) # add points to the coordinate system

angle_HH_RA_RC = np.tan((RC[2]-RA[2])/(RC[0]-RA[0]))
A_RC_RR_1 = getXYRotationMatrix(angle_HH_RA_RC)
A_RC_RR_2 = getTranslateMatrix(RC[0], RC[1], RC[2])
A_RC_RR = np.dot(A_RC_RR_2, A_RC_RR_1) # get the transformation matrix from coordinate system RC to RR

motorRR.updatePoints(motorRC, A_RC_RR)

motorRR.angle = np.pi/4
motorRR.rotatePoints() # rotate all the points

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

motorRR.plotAllPoints(ax)

ax.set_xlabel('X (in)')
ax.set_ylabel('Y (in)')
ax.set_zlabel('Z (in)')

ax.set_xlim3d(-15, 15)
ax.set_ylim3d(-15, 15)
ax.set_zlim3d(-15, 15)

plt.show()