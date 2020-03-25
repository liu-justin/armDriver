import CoordinateSystem as cs
import CoordinateSystemConstants as csc
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

csm = cs.coordinateSystemManager()

# RC has no children, so no args for it
motorRC = cs.coordinateSystem()
motorRR = cs.coordinateSystem(( motorRC, csc.A_RC_RR ))
motorRT = cs.coordinateSystem(( motorRR, csc.A_RR_RT ))

# adding points -----------------------------------------

motorRC.addPoint('CE', csc.CE)
motorRC.addPoint('BC', csc.BC)

motorRR.addPoint('RO', csc.RO)
motorRR.addPoint('RC', csc.RC)
motorRR.addPoint('OO', csc.OO)
motorRR.addPoint('RA', csc.RA)

# print(motorRR.points["BC"].homogeneous)
# print(motorRR.points["RO"].homogeneous)

# ar = motorRR.points["BC"].intersectionPoint(motorRR.points["RA"])
# print(ar)

csm.addCoordinateSystem(motorRC = motorRC, motorRR = motorRR, motorRT = motorRT)

# changing motor angles-----------------------------------------
csm.motorRC.angle = -np.pi/2
csm.motorRR.angle = np.pi/3 # rotate all the points in RC
csm.motorRT.angle = 0

# update the most parent coordinate system, it will propogate thru the rest
# if i can figure out if the coordinate system is a child of another, then i can make updatePoints from csm
# for now though, I have to use the seniorist parent
csm.motorRT.updatePoints()


# plotting --------------------------------------------------

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

motorRT.plotAllPoints(ax)

ax.set_xlabel('X (in)')
ax.set_ylabel('Y (in)')
ax.set_zlabel('Z (in)')

ax.set_xlim3d(-15, 15)
ax.set_ylim3d(-15, 15)
ax.set_zlim3d(-15, 15)

plt.show()