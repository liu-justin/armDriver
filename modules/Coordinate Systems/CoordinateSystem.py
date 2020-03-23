import numpy as np
import time
import CoordinateSystemConstants as csc

# each child can only have one parent, so should each coordinate system have a matrix to get to the parent coordinateSystem
# - no, because the coordinate system has no idea how to get to the parent coordinateSystem without the parents points
# alternative is passing in the matrix with the coordinateSystem in args

class coordinateSystem(object):
    def __init__(self, *args):
        self.points = {}
        self._angle = 0
        # z will always be the axis for rotation
        self.rotationMatrix = getRotationMatrix(0,0,self._angle)
        self.children = args # [tuple(coordinateSystem, matrix)]

    def addPointCoords(self, key, x, y=0, z=0):
        self.points[key] = np.array([x, y, z, 1])

    def addPoint(self, key, point):
        self.points[key] = point

    def rotatePointsTo(self, angle):
        self.angle = angle
        # self.points = {p:np.dot(self.rotationMatrix, self.points[p]) for p in self.points}
        self.points = {key:np.dot(self.rotationMatrix, value) for key,value in self.points.items()}

    def updatePoints(self):
        # for every child, create a dict of new transformed points based on the transformation that comes with the child, then update self.points
        for cs,matrix in self.children:
            newPoints = {key:np.dot(matrix, value) for key,value in cs.points.items()}

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

    def addCoordinateSystem(self,key, *args):
        self.coordinateSystemDict[key] = coordinateSystem(args)

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
