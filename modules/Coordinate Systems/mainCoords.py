import CoordinateSystem as cs
import CoordinateSystemConstants as csc
import pointFinderCoordinateSystem as pf
import Point as p
import numpy as np


csm = cs.coordinateSystemManager(csc.mainCS)

csm.addCoordinateSystem(motorRC = csc.motorRC, motorRR = csc.motorRR, motorRT = csc.motorRT)
# csm.plotAllPoints()
# changing motor angles-----------------------------------------
# csm.motorRC.angle = -np.pi/2
# csm.motorRR.angle = np.pi/3 # rotate all the points in RC
# csm.motorRT.angle = np.pi/5

# plotting --------------------------------------------------


angles = pf.findAngle2D(csm, 10, 0)
test = p.Point(10,0)
csm.mainCS.addPoint("TS", test)
# print(angles)
# csm.printAllAngles()
# csm.printAllPoints()
csm.plotAllPoints()
