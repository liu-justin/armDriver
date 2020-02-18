import modules.stepFinder as s
import modules.pointFinder as p
import modules.sendToArduinoStream as a
import modules.motor as motor
import modules.MotorList as MotorList

import time

def main():

	# test = p.Point(7,0)
	# result = p.findAngle2D(test)
	# print(result)
	mm = MotorList.MotorList()
	R0 = motor.Motor(mm)
	RA = motor.Motor(mm)
	#motorList = [R0, RA]

	# maybe I see when stepsInFrame = 0, and the starting tuple combined messes some stuff up

	while 1==1:
		first = p.Point(2,4)
		second = p.Point(3,8)

		p.linearTravel(first, second, mm)

		if mm[0].frameList == []:
		    print("angles is None, the linearTravel didn't go through the loop")
		    exit()
		else:
			#print(motorList[0].frameList)
			s.getSteps(mm)

			a.waitForArduino("{") # Arduino is ready! 
			a.initiateWithArduino(mm)
			while 1==1:
				a.communicateWithArduino(mm)

			#a.sendToArduinoDict(motorList)
		
main()
