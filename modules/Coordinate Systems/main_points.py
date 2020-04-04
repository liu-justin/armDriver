import Point as p
import numpy as np
import CoordinateSystem as cs

RA = p.Point("RA", 0,0, state = "fixed")
AB = p.Point("AB", 0,2.75)
BC = p.Point("BC", 9.49669118,2.49928784)
RC = p.Point("RC", 9.43702304,0, state = "fixed")
CE = p.Point("CE", 9.28188588, -6.49814839)
A = p.Link("A", 2.75, RA, AB)
B = p.Link("B", 9, AB, BC)
C = p.Link("C", 2.5, BC, RC)
R = p.Link("R", 9.7612, RA, RC)
Clower = p.Link("Clower", 6.5, RC, CE)

p.addRelation("collinear", Clower, C)

print(R.vectorFrom(RA))


motorRC = cs.coordinateSystem()
motorRC.addPoint("RA", RA)
motorRC.addPoint("AB", AB)
motorRC.addPoint("BC", BC)
motorRC.addPoint("RC", RC)
motorRC.addPoint("CE", CE)

A.changeAngle(2*np.pi/3, R)

print(BC.distanceTo(AB))
print(BC.distanceTo(RC))
motorRC.plotPoints()