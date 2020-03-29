import numpy as np
import math
import CoordinateSystem as cs
import Point as p


mainCS =  cs.coordinateSystem()

# first coordinate system, motor RT ----------------------------------------------------------------------

# points, motor RT has no additional points needed

# matrix to transfer from this coordinate system, to its parent mainCS, just identity
A_RT_main = cs.getRotationMatrix( 0 , 0 , 0 )

print("declaring motorRT now ------------------------------------------------------------------")
# declaring coordinate system and adding points
motorRT = cs.coordinateSystem(mainCS, A_RT_main)

# second coordinate system, motor RR ------------------------------------------------------------------

# points
RO = p.Point(0, 2.5)
RA = p.Circle(2.75, -2.40315424, 3.18909339)
RC = p.Point(6.99893387, 2.37783316)
OO = p.Point(0, 0)

# angle_RO_RR_RC = np.arccos(np.dot( RO.homogeneous[:-1] , RC.homogeneous[:-1] ) / (RO.magnitude() * RC.magnitude()) )
angle_RO_RR_RC = p.getAngleBetween(RO, OO, RC)
print(angle_RO_RR_RC)

# matrix to transfer from this coordinate system, to its parent RT
A_RR_RT = cs.getRotationMatrix( np.pi/2, 0, 0 )

# declaring coordinate system and adding points
print("declaring motorRR now ------------------------------------------------------------------")
motorRR = cs.coordinateSystem( motorRT, A_RR_RT )
motorRR.addPoint('RO', RO)
motorRR.addPoint('RC', RC)
motorRR.addPoint('OO', OO)
motorRR.addPoint('RA', RA)

# third coordinate system, motor RC ---------------------------------------------------------------

# points
CE = p.Point(6.5, 0)
BC = p.Circle(9.5, -2.5, 0)

# matrix to transfer from this coordinate system, to its parent RR
angle_HH_RA_RC = math.atan(( RC.y - RA.y )/( RC.x - RA.x ))   # angle_HH_RA_RC = -0.08607193
A_RC_RR_1 = cs.getRotationMatrix( 0, 0, angle_HH_RA_RC )
A_RC_RR_2 = cs.getTranslateMatrix( RC.x, RC.y, RC.z )
A_RC_RR = np.dot( A_RC_RR_2, A_RC_RR_1 )

# declaring coordinate system and adding points
print("declaring motorRC now ------------------------------------------------------------------")
motorRC = cs.coordinateSystem( motorRR, A_RC_RR )
motorRC.addPoint('CE', CE)
motorRC.addPoint('BC', BC)

# -------------------------------------------------------------------------------------------------------
# adding dependent point AB to motor RR
print("adding dependent point AB now -------------------------------------------------------------")

motorRR.addDependentPoint('AB', 'RA', 'BC')

# print("start of angle turning --------------------------------------------------------------")
# motorRC.angle = -2*np.pi/4

# after I set an angle, I need to update the parents; I cant have parents instead of children in Coordinate System,
# because the child doesnt know how to get to where it needs to be in the parent coordinate system
# motorRR.angle = np.pi/3
# motorRR.angle = -np.pi/6
# motorRT.angle = np.pi/7
# cs.printPoints(mainCS.points)
# mainCS.plotPoints()