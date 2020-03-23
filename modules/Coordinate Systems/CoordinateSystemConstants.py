import numpy as np

def toPoint(x,y,z=0):
    return np.array([x,y,z,1])

CE = toPoint(6, 0)
BC = toPoint(-2, 0)

# second coordinate system ---------------------------------

RO = toPoint(0, 2.5)
RA = toPoint(-2.40315424, 3.18909339)
RC = toPoint(6.99893387, 2.37783316)
OO = toPoint(0, 0)

