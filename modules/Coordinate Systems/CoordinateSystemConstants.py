import numpy as np
import math
import CoordinateSystem as cs
import Point as p

def toPoint(x,y,z=0):
    return np.array([x,y,z,1])

# first coordinate system, motor RC ---------------------------------------------------------------

# points
CE = p.Point(6.5, 0)
BC = p.Circle(9.5, -2.5, 0)

# matrix for children of this coordinate system, motor RC has no children
# declaring coordinate system and adding points
print("")
print("creating RC coordinate system")
motorRC = cs.coordinateSystem()
motorRC.addPoint('CE', CE)
motorRC.addPoint('BC', BC)

# second coordinate system, motor RR ------------------------------------------------------------------

# points
RO = p.Point(0, 2.5)
RA = p.Circle(2.75, -2.40315424, 3.18909339)
RC = p.Point(6.99893387, 2.37783316)
OO = p.Point(0, 0)

angle_RO_RR_RC = np.arccos(np.dot(RO.regular, RC.regular)/(RO.magnitude()*RC.magnitude()))

# matrix for children of this coordinate system, only RC
angle_HH_RA_RC = np.tan(( RC.y - RA.y )/( RC.x - RA.x ))
A_RC_RR_1 = cs.getRotationMatrix( 0, 0, angle_HH_RA_RC )
A_RC_RR_2 = cs.getTranslateMatrix( RC.x, RC.y, RC.z )
A_RC_RR = np.dot( A_RC_RR_2, A_RC_RR_1 )

# declaring coordinate system and adding points
print(" ")
print("creating RR coordinate system")
motorRR = cs.coordinateSystem(( motorRC, A_RC_RR ))
print("This is RC after creation of RR, checking for to see if RC points are updated")
print([(a[0], a[1].homogeneous) for a in motorRC.points.items()])
motorRR.addPoint('RO', RO)
motorRR.addPoint('RC', RC)
motorRR.addPoint('OO', OO)
motorRR.addPoint('RA', RA)

# motorRR.updatePoints()

# third coordinate system, motor RT ----------------------------------------------------------------------

# points, motor RT has no additional points needed

# matrix for children of this coordinate system, only RR
A_RR_RT = cs.getRotationMatrix( np.pi/2, 0, 0 )

# declaring coordinate system and adding points
print("")
print("creating RT coordinate system")
motorRT = cs.coordinateSystem(( motorRR, A_RR_RT ))

# -------------------------------------------------------------
