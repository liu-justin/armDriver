import CoordinateSystem as cs
import CoordinateSystemConstants as csc
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# RC has no children, so no args for it
motorRC = cs.coordinateSystem()
motorRR = cs.coordinateSystem(( motorRC, csc.A_RC_RR ))
motorRT = cs.coordinateSystem(( motorRR, csc.A_RR_RT ))

# adding points -----------------------------------------

motorRC.addPoint('CE', csc.CE)
motorRC.addPoint('BC', csc.BC)

motorRR.addPoint('RO', csc.RO)
motorRR.addPoint('RA', csc.RA)
motorRR.addPoint('RC', csc.RC)
motorRR.addPoint('OO', csc.OO)

# changing motor angles-----------------------------------------
motorRC.angle = -np.pi/4
motorRR.angle = np.pi/8 # rotate all the points in RC
motorRT.angle = -np.pi/3

# update the most parent coordinate system, it will propogate thru the rest
motorRT.updatePoints()


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