import numpy as np

class WeightManager:
    def __init__(self):
        self.pointList = []
        self.torquePlot = [] # x,y,torque

    def appendPoint(self, point, weight):
        # format for the deterimant, point x and point y on top, weight force hori = 0, weight force vert)
        weightFormat = np.array([[point.x, point.y], [0,-weight]])
        self.pointList.append(weightFormat)
    
    def appendTorquePlot(self, testX, testY):
        self.torquePlot.append((testX, testY, self.calcTorque()))

    def clear(self):
        self.pointList = []


    def calcTorque(self):
        totalTorque = 0
        for i in self.pointList:
            totalTorque += np.linalg.det(i)

        return totalTorque