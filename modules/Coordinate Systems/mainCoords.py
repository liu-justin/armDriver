import CoordinateSystem as cs
import CoordinateSystemConstants as csc
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

csm = cs.coordinateSystemManager(csc.mainCS)

csm.addCoordinateSystem(motorRC = csc.motorRC, motorRR = csc.motorRR, motorRT = csc.motorRT)
# csm.plotAllPoints()
# changing motor angles-----------------------------------------
csm.motorRC.angle = -np.pi/2
csm.motorRR.angle = np.pi/3 # rotate all the points in RC
csm.motorRT.angle = np.pi/5

# a = csm.findPointMain("CE")
# cs.printPoints(csm.mainCS.points)
# plotting --------------------------------------------------

csm.plotAllPoints()
