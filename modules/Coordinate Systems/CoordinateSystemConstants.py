import numpy as np
import math
import CoordinateSystem as cs
import Point as p



# first coordinate system, motor RT ----------------------------------------------------------------------

# points, motor RT has no additional points needed

# matrix to transfer from this coordinate system, to its parent, which it has none

print("declaring motorRT now ------------------------------------------------------------------")
# declaring coordinate system and adding points
motorRT = cs.coordinateSystem()

# second coordinate system, motor RR ------------------------------------------------------------------

# points
RO = p.Point(0, 2.5)
RA = p.Circle(2.75, -2.40315424, 3.18909339)
RC = p.Point(6.99893387, 2.37783316)
OO = p.Point(0, 0)

angle_RO_RR_RC = np.arccos(np.dot(RO.homogeneous[:-1], RC.homogeneous[:-1])/(RO.magnitude()*RC.magnitude()))

# matrix to transfer from this coordinate system, to its parent RT
A_RR_RT = cs.getRotationMatrix( np.pi/2, 0, 0 )

# declaring coordinate system and adding points
print("declaring motorRR now ------------------------------------------------------------------")
motorRR = cs.coordinateSystem( motorRT, A_RR_RT )
motorRR.addPoint('RO', RO)
motorRR.addPoint('RC', RC)
motorRR.addPoint('OO', OO)
motorRR.addPoint('RA', RA)
print(f"this is motorRT points: {motorRT.points}")


# third coordinate system, motor RC ---------------------------------------------------------------

# points
CE = p.Point(6.5, 0)
BC = p.Circle(9.5, -2.5, 0)

# matrix to transfer from this coordinate system, to its parent RR
angle_HH_RA_RC = np.tan(( RC.y - RA.y )/( RC.x - RA.x ))
A_RC_RR_1 = cs.getRotationMatrix( 0, 0, angle_HH_RA_RC )
A_RC_RR_2 = cs.getTranslateMatrix( RC.x, RC.y, RC.z )
A_RC_RR = np.dot( A_RC_RR_2, A_RC_RR_1 )

# matrix for children of this coordinate system, motor RC has no children
# declaring coordinate system and adding points
print("declaring motorRC now ------------------------------------------------------------------")
motorRC = cs.coordinateSystem( motorRR, A_RC_RR )
motorRC.addPoint('CE', CE)
motorRC.addPoint('BC', BC)

# -------------------------------------------------------------------------------------------------------
# adding dependent point AB to motor RR
print("adding dependent point AB now -------------------------------------------------------------")
# AB = motorRR.points["RA"].intersectionPoint(motorRR.points["BC"])
# motorRR.addPoint('AB', AB)

# motorRR.addDependentPoint('AB', 'RA', 'BC')

# print(motorRR.points["AB"])
# print(motorRR.points["RA"])
# print(motorRR.points["BC"])
# print("distancing")
# print(motorRR.points["AB"].distanceTo(motorRR.points["RA"]))
# print(motorRR.points["AB"].distanceTo(motorRR.points["BC"]))
# print(f"RA radius: {RA.radius}, BC radius: {BC.radius}")


print("start of angle turning --------------------------------------------------------------")
motorRC.angle = -2*np.pi/4

# # # after I set an angle, I need to update the parents; I cant have parents instead of children in Coordinate System,
# # # because the child doesnt know how to get to where it needs to be in the parent coordinate system
motorRR.angle = np.pi/3
motorRT.angle = -np.pi/4
cs.printPoints(motorRT.points)
motorRT.plotPoints()