import numpy as np
import time
import Point as p
import copy 

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# each child can only have one parent, so should each coordinate system have a matrix to get to the parent coordinateSystem
# - no, because the coordinate system has no idea how to get to the parent coordinateSystem without the parents points
# alternative is passing in the matrix with the coordinateSystem in args

class coordinateSystem(object):
    def __init__(self, *args):
        self.points = {}
        self.dependents = {}
        self._angle = 0
        # z will always be the axis for rotation
        self.rotationMatrix = getRotationMatrix(0,0,self._angle)
        self.parent = args # [tuple(coordinateSystem, matrix)]

    def addPoint(self, key, point):
        self.points[key] = point
        self.updatePoints()

    def addDependentPoint(self, key, pointA, pointB):
        self.dependents[key] = (pointA, pointB)
        self.points[key] = self.points[pointA].intersectionPoint(self.points[pointB])
        self.updatePoints()

    def rotatePoints(self): # looks like if I want to use Points, i have to edit the dict values instead of make a new dict; alternative was np.array
        # self.points = {key:np.dot(self.rotationMatrix, value) for key,value in self.points.items()}
        for point in self.points.values():
            point.homogeneous = np.dot(self.rotationMatrix, point.homogeneous)
        # self.points = {key:p.Point(np.dot(self.rotationMatrix, value))for key,value in self.points.items()}

    def updateDependents(self):
        newDependents = {key:self.points[value[0]].intersectionPoint(self.points[value[1]]) for key, value in self.dependents.items()}
        print(newDependents)
        self.points.update(newDependents)

    def updatePoints(self): # recursively update parents with new points
        if (not self.parent):
            print("zero case for updating Parent direction")
            return

        self.updateDependents()

        # create a copy of self.points to modify with matrices and send to parents
        newPoints = {key:copy.deepcopy(value) for key,value in self.points.items()}
        for point in newPoints.values():
            point.homogeneous = np.dot(self.parent[1], np.dot(self.rotationMatrix, point.homogeneous))

        # for k,v in newPoints.items():
        #     newPoints[k].homogeneous = np.dot(self.parent[1], np.dot(self.rotationMatrix, newPoints[k].homogeneous))
        #     newPoints[k].regular = newPoints[k].homogeneous[:-1]

        # then transfer the points to parents
        self.parent[0].points.update(newPoints)
        # then let the parents update their parents
        self.parent[0].updatePoints()

        return

    def plotPoints(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for k,v in self.points.items():
            ax.scatter3D(v.homogeneous[0], v.homogeneous[1], v.homogeneous[2])
            ax.text(v.homogeneous[0], v.homogeneous[1], v.homogeneous[2], k)

        ax.set_xlabel('X (in)')
        ax.set_ylabel('Y (in)')
        ax.set_zlabel('Z (in)')

        ax.set_xlim3d(-15, 15)
        ax.set_ylim3d(-15, 15)
        ax.set_zlim3d(-15, 15)

        plt.show()

    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, a):
        print("setting angle to : %s", a)
        self._angle = a - self._angle
        # this reassignment has around the same runtime as reassigning each entry individually
        self.rotationMatrix = getRotationMatrix(0,0,self._angle)
        self.updatePoints()
        self.rotatePoints()

class coordinateSystemManager(coordinateSystem):
    def __init__(self):
        self.coordinateSystemDict = {}

    def addCoordinateSystem(self, **kwargs):
        # self.coordinateSystemDict.update(kwargs)
        self.__dict__.update(kwargs)

    def plotAllPoints(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        motorRT.plotPoints()

        ax.set_xlabel('X (in)')
        ax.set_ylabel('Y (in)')
        ax.set_zlabel('Z (in)')

        ax.set_xlim3d(-15, 15)
        ax.set_ylim3d(-15, 15)
        ax.set_zlim3d(-15, 15)

        plt.show()

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

def printPoints(points):
    print("<<<")
    for k,v in points.items():
        print(f"{k}: {v}")
    print(">>>")