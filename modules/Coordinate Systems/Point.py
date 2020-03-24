import numpy as np
import math

class Point:
    def __init__(self, *args):
        if (isinstance(args[0], (int, float))):
            self.nparray = args[0]
            self.x = args[0][0]
            self.y = args[0][1]
            self.z = args[0][2]
        else:
            self.x = args[0]
            self.y = args[1]
            self.z = 0 if len(args)==2 else args[2]
            
            self.nparray = np.array([self.x,self.y,self.z,1])

        self.normalarray = self.nparray[:-1]

    
    def mag(self):
        return math.sqrt( self.x**2 + self.y**2 + self.z**2 )