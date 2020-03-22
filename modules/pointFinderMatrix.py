import basicShapes as bs
import stepMath as smath
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ORIGIN = np.array([0,0,0,1])

# got from solidworks skeleton main, when RO-RR is vertical and RR is 0,0
RO = np.array([0, 0, 2.5, 1])
RA = np.array([-2.40315424, 0, 3.18909339, 1])
RC = np.array([6.99893387, 0, 2.37783316, 1])

angle_HH_RA_RC = np.tan((RC[2]-RA[2])/(RC[0]-RA[0]))
A_RC_rotation = np.array([[np.cos(angle_HH_RA_RC), 0, -np.sin(angle_HH_RA_RC), 0],
                          [                     0, 1,                       0, 0],
                          [np.sin(angle_HH_RA_RC), 0,  np.cos(angle_HH_RA_RC), 0],
                          [                     0, 0,                       0, 1]])
A_RC_translate = np.array([[1,0,0,RC[0]],
                           [0,1,0,RC[1]],
                           [0,0,1,RC[2]],
                           [0,0,0,    1]])
A_RC_RR = np.dot(A_RC_translate, A_RC_rotation)
length_RC_CE = 6
CE = np.array([6, 0, 0, 1])

class coordinateSystem(object):
    def __init__(self, m):
        self.points = []
        self._angle = 0
        self.rotationMatrix = np.array([[np.cos(self._angle), -np.sin(self._angle)],
                                        [np.sin(self._angle), np.cos(self._angle)]])

    def addPoint(self, point):
        self.points.append(point)

    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, a):
        self._angle = a

def rotateRT(angleRT):
    return np.array([[ np.cos(angleRT), -np.sin(angleRT), 0, 0],
                     [np.sin(angleRT) , np.cos(angleRT) , 0, 0],
                     [0               ,                0, 1, 0],
                     [0               ,                0, 0, 1]])

def rotateRR(angleRR):
    return np.array([[np.cos(angleRR) , 0, np.sin(angleRR), 0],
                     [0               , 1,               0, 0],
                     [-np.sin(angleRR), 0, np.cos(angleRR), 0],
                     [0               , 0,               0, 1]])

def rotateRC(angleRC):
    return np.array([[np.cos(angleRC) , 0, -np.sin(angleRC), 0],
                     [0               , 1,               0, 0],
                     [np.sin(angleRC), 0, np.cos(angleRC), 0],
                     [0               , 0,               0, 1]])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in np.arange(0, 25*1.8*np.pi/180, 5*1.8*np.pi/180):

    #rotation at RC motor
    angleRC = -np.pi/2
    A_RC = rotateRC(angleRC)
    CE_new = np.dot(A_RC, CE)
    CE_new = np.dot(A_RC_RR, CE_new)

    # rotation at RR motor
    angleRR = -i
    A_RR = rotateRR(angleRR)

    RO_new = np.dot(A_RR, RO)
    RA_new = np.dot(A_RR, RA)
    RC_new = np.dot(A_RR, RC)
    CE_new = np.dot(A_RR, CE_new)

    # rotation theta at the bottom
    angleRT = i
    A_RT = rotateRT(angleRT)

    RO_new = np.dot(A_RT, RO_new)
    RA_new = np.dot(A_RT, RA_new)
    RC_new = np.dot(A_RT, RC_new)
    CE_new = np.dot(A_RT, CE_new)

    plotting_array = np.array([ORIGIN, RO_new, RA_new, RO_new, RC_new, CE_new, RC_new, RO_new, ORIGIN])
    ax.plot3D(plotting_array[:,0], plotting_array[:,1], plotting_array[:,2])


ax.set_xlabel('X (in)')
ax.set_ylabel('Y (in)')
ax.set_zlabel('Z (in)')

ax.set_xlim3d(-15, 15)
ax.set_ylim3d(-15, 15)
ax.set_zlim3d(-15, 15)

plt.show()