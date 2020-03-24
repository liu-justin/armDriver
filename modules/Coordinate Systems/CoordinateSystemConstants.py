import numpy as np
import math
import CoordinateSystem as cs
import Point as p

def toPoint(x,y,z=0):
    return np.array([x,y,z,1])

lengthB = 9.5
lengthA = 2.75

# first coordinate system, motor RC ---------------------------------------------------------------

# points
CE = p.Point(6.5, 0)
BC = p.Point(-2.5, 0)

# matrix for children of this coordinate system, motor RC has no children

# second coordinate system, motor RR ------------------------------------------------------------------

# points
RO = p.Point(0, 2.5)
RA = p.Point(-2.40315424, 3.18909339)
RC = p.Point(6.99893387, 2.37783316)
OO = p.Point(0, 0)

angle_RO_RR_RC = np.arccos(np.dot(RO.normalarray, RC.normalarray)/(RO.mag()*RC.mag()))

# matrix for children of this coordinate system, only RC
angle_HH_RA_RC = np.tan(( RC.y - RA.y )/( RC.x - RA.x ))
A_RC_RR_1 = cs.getRotationMatrix( 0, 0, angle_HH_RA_RC )
A_RC_RR_2 = cs.getTranslateMatrix( RC.x, RC.y, RC.z )
A_RC_RR = np.dot( A_RC_RR_2, A_RC_RR_1 )

# third coordinate system, motor RT ----------------------------------------------------------------------

# points, motor RT has no additional points needed

# matrix for children of this coordinate system, only RR
A_RR_RT = cs.getRotationMatrix( np.pi/2, 0, 0 )

