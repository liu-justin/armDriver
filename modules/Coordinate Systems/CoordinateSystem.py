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
        self.dependents = {} # key is pointName, value is (pointA, pointB) for the points it depends on
        self.children = [] # other CS

        self._angle = 0
        # z will always be the axis for rotation
        self.rotationMatrix = getRotationMatrix(0,0,self._angle)

        if not args:
            self.parent = None
            self.parentMatrix = None
        else:
            self.parent = args[0]
            self.parentMatrix = args[1]
            self.parent.children.append(self)

    def addPoint(self, key, point):
        self.points[key] = point
        # self.updatePoints()

    def addDependentPoint(self, key, pointA, pointB):
        self.dependents[key] = (pointA, pointB)
        self.updateDependentsOnly()
        # self.points[key] = self.points[pointA].intersectionPoint(self.points[pointB])
        # self.updatePoints()

    # def rotatePoints(self): # looks like if I want to use Points, i have to edit the dict values instead of make a new dict; alternative was np.array
    #     # self.points = {key:np.dot(self.rotationMatrix, value) for key,value in self.points.items()}
    #     for point in self.points.values():
    #         point.homogeneous = np.dot(self.rotationMatrix, point.homogeneous)
    #     # self.points = {key:p.Point(np.dot(self.rotationMatrix, value))for key,value in self.points.items()}

    # def updateDependents(self): # if the points that these point depends on changes, this will update those dependent points 
    #     newDependents = {key:self.points[value[0]].intersectionPoint(self.points[value[1]]) for key, value in self.dependents.items()}
    #     self.points.update(newDependents)

    # def updatePoints(self): # recursively update parents with new points
    #     if (not self.parent): # zero case for recursion, if self doesn't have a parent, meaning its mainCS
    #         return

    #     self.updateDependents()

    #     newPoints = {key:copy.deepcopy(value) for key,value in self.points.items()} # create a deep copy of self.points
    #     for point in newPoints.values():                                            # transform it with rotation and parent matrices
    #         point.homogeneous = np.dot(self.parentMatrix, np.dot(self.rotationMatrix, point.homogeneous)) 

    #     self.parent.points.update(newPoints) # then transfer the points to parents
    #     self.parent.updatePoints() # then let the parents update their parents
    #     return

    def findCSOfPoint(self, p):
        print(p)
        print(self.points.keys())
        if p in self.points.keys():
            return self
        if self.children == []:
            return None
        for child in self.children:
            return child.findCSOfPoint(p)

    def transformPoint(self, p): # returns the transformed point, point must be in this coordinate system or its children
        coord = self.findCSOfPoint(p)
        newPoint = copy.deepcopy(coord.points[p])
        while coord != self:
            newPoint.homogeneous = np.dot(coord.parentMatrix, np.dot(coord.rotationMatrix, newPoint.homogeneous))
            coord = coord.parent
        return newPoint

    def updateDependentsOnly(self):
        # key is the actual point, value is the points that are needed for intersectionPoint
        for key, value in self.dependents.items():
            a = self.transformPoint(value[0])
            print(a)
            b = self.transformPoint(value[1])
            print(b)
            print("finished getting both points")

            self.points[key] = a.intersectionPoint(b)

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
        self._angle = a
        # this reassignment has around the same runtime as reassigning each entry individually
        self.rotationMatrix = getRotationMatrix(0,0,self._angle)
        self.updateDependentsOnly()
        # self.updatePoints()
        # self.rotatePoints()

class coordinateSystemManager(coordinateSystem):
    def __init__(self, mainCS):
        self.csDict = {}
        self.mainCS = mainCS

    def addCoordinateSystem(self, **kwargs):
        self.csDict.update(kwargs)
        # self.__dict__.update(kwargs)

    def plotAllPoints(self):
        self.mainCS.plotPoints()

    def findPointCS(self, pointa):
        for coord in self.csDict.values():
            if pointa in coord.points.keys():
                return coord

    def findPointMain(self, pointa):
        coord = self.findPointCS(pointa)
        transformedPoint = np.dot(coord.parentMatrix, np.dot(coord.rotationMatrix, coord.points[pointa].homogeneous))
        coord = coord.parent
        while coord != self.mainCS:
            transformedPoint = np.dot(coord.parentMatrix, np.dot(coord.rotationMatrix, transformedPoint))
            coord = coord.parent
        return transformedPoint            


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
