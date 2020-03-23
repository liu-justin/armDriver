import CoordinateSystem as cs
import CoordinateSystemConstants as csc
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# RC has no children, so no args for it
motorRC = cs.coordinateSystem()

# RR has one child, RC: args has the tuple (coordinate system, matrix to get from RC to RR)
angle_HH_RA_RC = np.tan(( csc.RC[1] - csc.RA[1] )/( csc.RC[0] - csc.RA[0] ))
A_RC_RR_1 = cs.getRotationMatrix( 0, 0, angle_HH_RA_RC )
A_RC_RR_2 = cs.getTranslateMatrix( csc.RC[0], csc.RC[1], csc.RC[2] )
A_RC_RR = np.dot( A_RC_RR_2, A_RC_RR_1 ) # get the transformation matrix from coordinate system RC to RR

motorRR = cs.coordinateSystem(( motorRC, A_RC_RR ))

# RT has one child, RR
A_RR_RT = cs.getRotationMatrix( np.pi/2, 0, 0 )

motorRT = cs.coordinateSystem(( motorRR, A_RR_RT ))

# adding points -----------------------------------------

motorRC.addPoint('CE', csc.CE)
motorRC.addPoint('BC', csc.BC)

motorRR.addPoint('RO', csc.RO)
motorRR.addPoint('RA', csc.RA)
motorRR.addPoint('RC', csc.RC)
motorRR.addPoint('OO', csc.OO)

# changing motor angles-----------------------------------------
motorRC.angle = -np.pi/2
motorRR.angle = np.pi/4 # rotate all the points in RC
motorRT.angle = np.pi/3

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