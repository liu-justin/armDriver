import modules.stepFinder as s
import modules.pointFinder as p
#import modules.sendToArduinoStream as a
import modules.motor as motor
import modules.MotorList as MotorList
import modules.basicShapes as bs

import time

def main():

	mm = MotorList.MotorList()
	R0 = motor.Motor(mm)
	RA = motor.Motor(mm)
	#motorList = [R0, RA]

	testingTimes = []

	#while 1==1:
	first = bs.Point(10,-4)
	second = bs.Point(10,-1)
	testingTimes.append(time.perf_counter())
	p.linearTravel(first, second, mm)
	testingTimes.append(time.perf_counter())

	if mm[0].frameList == []:
		print("angles is None, the linearTravel didn't go through the loop")
		exit()
	else:
		s.getSteps(mm)
		testingTimes.append(time.perf_counter())

		# a.waitForArduino("{") # Arduino is ready! 
		# a.initiateWithArduino(mm)
		# while 1==1:
		# 	a.communicateWithArduino(mm)

	testingDifference = [j-i for i,j in zip(testingTimes[:-1], testingTimes[1:])]
	print(testingDifference)
	print(testingDifference[1]/testingDifference[0])

		
main()
