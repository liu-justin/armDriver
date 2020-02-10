import modules.stepFinder as s
import modules.pointFinder as p
#import modules.sendToArduinoStream as a
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
		print(motorList[0].stepTuple)
		

#		a.waitForArduino("Arduino is ready!")
#		a.initiateWithArduino(motorList)
#		while 1==1:
#			a.communicateWithArduino(motorList)

		#a.sendToArduinoDict(motorList)
		
main()
