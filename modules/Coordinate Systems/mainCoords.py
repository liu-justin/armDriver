import CoordinateSystem as cs
import CoordinateSystemConstants as csc
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

csm = cs.coordinateSystemManager(csc.mainCS)

csm.addCoordinateSystem(motorRC = csc.motorRC, motorRR = csc.motorRR, motorRT = csc.motorRT)
print(csm.csDict)
# changing motor angles-----------------------------------------
csm.csDict["motorRC"].angle = -np.pi/2
csm.csDict["motorRR"].angle = np.pi/3 # rotate all the points in RC
csm.csDict["motorRT"].angle = 0

a = csm.findPoint("CE")
print(a)
cs.printPoints(csm.mainCS.points)
# plotting --------------------------------------------------

# csm.plotAllPoints()
