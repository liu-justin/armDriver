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

test = p.Point(5,0,7)
angles = pf.findAngle2D(csm, test)

csm.mainCS.addPoint("TS", test)
# print(angles)
# csm.printAllAngles()
# csm.printAllPoints()
print("distance from TS to RC: ", csm["TS"].distanceTo(csm["RC"]))
csm.plotAllPoints()
