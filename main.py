import modules.stepFinder as s
import modules.pointFinder as p
#import modules.sendToArduino as s
import modules.motor as motor

import time

def main():
	#singlePoint(1,9)
	#multiplePoint()

	R0 = motor.Motor(0)
	RA = motor.Motor(1)
	#N17 = motor.Motor(2)
	#Theta = motor.Motor(3)
	motorList = [R0, RA]

	startTime = time.perf_counter()

	first = p.Point(2, 9)
	second = p.Point(2,-9)

	p.linearTravel(first, second, motorList)

	afterLTTime = time.perf_counter()

	if motorList[0].frameList == []:
	    print("angles is None, the linearTravel didn't go through the loop")
	    exit()
	else:
		s.getSteps(motorList)

		#s.waitForArduino()
		#s.sendToArduino(data[0], data[1], data[2], data[3])

		afterGSTime = time.perf_counter()

	#print(f"{afterLTTime - startTime} : {afterGSTime - afterLTTime}")

main()
