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
    def __init__(self, parent = None, parentMatrix = None):
        self.points = {}
        self.dependents = {} # key is pointName, value is (pointA, pointB) for the points it depends on
        self.children = [] # other CS, type is CS
        self.siblings = [] # other CS, type is CS

        self._angle = 0
        # z will always be the axis for rotation
        self.rotationMatrix = getRotationMatrix(0,0,self._angle)

        self.parent = parent
        self.parentMatrix = parentMatrix
        if self.parent != None:
            self.siblings.extend(self.parent.children)
            self.parent.children.append(self)
            

    def addPoint(self, key, point):
        self.points[key] = point

    def addDependentPoint(self, key, pointA, pointB):
        self.dependents[key] = (pointA, pointB)
        self.updateDependentsOnly()

    def findCSOfPoint(self, p):
        if p in self.points.keys():
            return self
        if self.children == []: # if this coordinate system doesn't have any children
            return None
        for child in self.children:
            return child.findCSOfPoint(p)

    def transformPointUsingName(self, p, coord = None): # returns the transformed point, point must be in this coordinate system or its children
        if coord == None:
            coord = self.findCSOfPoint(p)
        # coord = self.findCSOfPoint(p)
        newPoint = copy.deepcopy(coord.points[p])
        while coord != self:
            newPoint.homogeneous = np.dot(coord.parentMatrix, np.dot(coord.rotationMatrix, newPoint.homogeneous))
            coord = coord.parent
        return newPoint

    def transformPointUsingPoint(self, p, coord): # only if you know the point and coord directly, use this one; otherwise use the one above
        newPoint = copy.deepcopy(p)
        while coord != self:
            newPoint.homogeneous = np.dot(coord.parentMatrix, np.dot(coord.rotationMatrix, newPoint.homogeneous))
            coord = coord.parent
        return newPoint

    def updateDependentsOnly(self): # recursively updates all the points that are dependent on other points, not fixed in space
        if (self.parent == None): # zero case
            return
        # key is the actual point, value is the points that are needed for intersectionPoint
        for key, value in self.dependents.items():
            a = self.transformPointUsingName(value[0]) # a/b are the two points that key depends on
            b = self.transformPointUsingName(value[1])

            self.points[key] = a.intersectionPoint(b)
        
        self.parent.updateDependentsOnly()

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


class coordinateSystemManager(object):
    def __init__(self, mainCS):
        self.mainCS = mainCS

    def addCoordinateSystem(self, **kwargs):
        # self.csDict.update(kwargs)
        # for cs in kwargs.values():
        #     self.pointNames.extend(cs.points.keys())
        
        # replaced __dict__ with vars(self)
        vars(self).update(kwargs)
    
    def __getitem__(self, name):
        return self.findPointMain(name) 

    def plotAllPoints(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for coord in vars(self).values():
            for name, point in coord.points.items():
                newPoint = self.mainCS.transformPointUsingPoint(point, coord)
                ax.scatter3D(newPoint.homogeneous[0], newPoint.homogeneous[1], newPoint.homogeneous[2])
                ax.text(newPoint.homogeneous[0], newPoint.homogeneous[1], newPoint.homogeneous[2], name)

        ax.set_xlabel('X (in)')
        ax.set_ylabel('Y (in)')
        ax.set_zlabel('Z (in)')

        ax.set_xlim3d(-15, 15)
        ax.set_ylim3d(-15, 15)
        ax.set_zlim3d(-15, 15)

        plt.show()
    
    def printAllPoints(self):
        print("<<<")
        for coord in vars(self).values():
            for name, point in coord.points.items():
                newPoint = self.mainCS.transformPointUsingPoint(point, coord)
                print(f"{name}: {newPoint}")
        print(">>>")

    def printAllAngles(self):
        print("ALL ANGLES<<<")
        for name, coord in vars(self).items():
            print(f"{name}: {coord.angle}")
        print(">>>")


    def findCSMain(self, p):
        for coord in vars(self).values():
            if p in coord.points.keys():
                return coord

    def findPointMain(self, p, coord=None):
        # coord = self.findPointCS(p)
        # transformedPoint = np.dot(coord.parentMatrix, np.dot(coord.rotationMatrix, coord.points[p].homogeneous))
        # coord = coord.parent
        # while coord != self.mainCS:
        #     transformedPoint = np.dot(coord.parentMatrix, np.dot(coord.rotationMatrix, transformedPoint))
        #     coord = coord.parent
        # return transformedPoint
        if coord == None:
            coord = self.findCSMain(p)
        newPoint = copy.deepcopy(coord.points[p])
        while coord != self.mainCS:
            newPoint.homogeneous = np.dot(coord.parentMatrix, np.dot(coord.rotationMatrix, newPoint.homogeneous))
            coord = coord.parent
        return newPoint     


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
