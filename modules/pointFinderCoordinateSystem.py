import numpy as np
import time

class coordinateSystem(object):
    def __init__(self):
        self.points = []
        self._angle = 0
        self.rotationMatrix = np.array([[np.cos(self._angle), -np.sin(self._angle)],
                                        [np.sin(self._angle), np.cos(self._angle)]])

    def addPoint(self, point):
        self.points.append(point)

    def rotatePoints(self):
        self.points = [np.dot(self.rotationMatrix, p) for p in self.points]

    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, a):
        self._angle = a
        # this reassignment has around the same runtime as reassigning each entry individually
        self.rotationMatrix = np.array([[np.cos(self._angle), -np.sin(self._angle)],
                                        [np.sin(self._angle), np.cos(self._angle)]])

cs1 = coordinateSystem()
cs1.angle = np.pi/4
RO = np.array([0, 2.5])
RA = np.array([-2.40315424, 3.18909339])
RC = np.array([6.99893387, 2.37783316])
cs1.addPoint(RO)
cs1.addPoint(RA)
cs1.addPoint(RC)
cs1.rotatePoints()
print(cs1.points)