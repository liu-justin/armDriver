import modules.stepFinder as s
import modules.pointFinder as p
import modules.sendToArduino as a
import modules.motor as motor

import time

def main():

	R0 = motor.Motor(0)
	RA = motor.Motor(1)
	motorList = [R0, RA]

	first = p.Point(12, 2)
	second = p.Point(5,-8)

	p.linearTravel(first, second, motorList)

	if motorList[0].frameList == []:
	    print("angles is None, the linearTravel didn't go through the loop")
	    exit()
	else:
		s.getSteps(motorList)

		a.waitForArduino()
		a.sendToArduinoDict(motorList)

main()
