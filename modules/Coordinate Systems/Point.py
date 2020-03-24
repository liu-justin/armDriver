import numpy as np
import math

class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.homogeneous = np.array([x,y,z,1])
        self.regular = self.homogeneous[:-1]

    
    def mag(self):
        return math.sqrt( self.x**2 + self.y**2 + self.z**2 )