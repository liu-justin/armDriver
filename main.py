import modules.stepFinder as s
import modules.pointFinder as p
import modules.sendToArduino as a
import modules.motor as motor

import time

def main():

	# test = p.Point(7,0)
	# result = p.findAngle2D(test)
	# print(result)

	R0 = motor.Motor(0)
	RA = motor.Motor(1)
	motorList = [R0, RA]

	first = p.Point(9.581, 5.085)
	second = p.Point(5,0)

	p.linearTravel(first, second, motorList)

	if motorList[0].frameList == []:
	    print("angles is None, the linearTravel didn't go through the loop")
	    exit()
	else:
		s.getSteps(motorList)

		a.waitForArduino("s6")
		a.sendToArduinoDict(motorList)
		
main()
