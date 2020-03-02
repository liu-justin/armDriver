#!/usr/bin/env python

from v1_3axis.srv import *
import rospy

import stepFinder as s
import pointFinder as p
import Motor
import MotorList
import math
import numpy as np

def handle_endpoints_to_steps(req):
    first = p.Point(req.startPointX, req.startPointY)
    second = p.Point(req.endPointX, req.endPointY)
    p.linearTravel(first, second, mm)
    print(mm[0].frameList)
    s.getSteps(mm)
    print(mm[0].stepTuple)
    testA = [1.1,2.23,3.251,4.124]
    testB = [3.2411,4.5215,5.1525,6.12414]
    return EndpointsToStepsResponse(testA, testB)

def handle_steps_to_arduino(req):
    nextSet = mm[req.startByte].stepTuple.pop()
    return NextStepResponse(nextSet[2], nextSet[3])

def endpoints_to_steps_server():
    rospy.init_node('endpoints_to_steps_server')
    s = rospy.Service('endpoints_to_steps', EndpointsToSteps, handle_endpoints_to_steps)
    s2 = rospy.Service("fetching_next_steps", NextStep, handle_steps_to_arduino)
    print "Convert Endpoints to steps and start stepping."
    rospy.spin()

if __name__ == "__main__":
    mm = MotorList.MotorList()
    R0 = Motor.Motor(mm)
    RA = Motor.Motor(mm)
	#motorList = [R0, RA]

	# #while 1==1:
	# first = p.Point(10,-4)
	# second = p.Point(10,-1)
	# p.linearTravel(first, second, mm)

	# if mm[0].frameList == []:
	# 	print("angles is None, the linearTravel didn't go through the loop")
	# 	exit()
	# else:
	# 	s.getSteps(mm)

	# 	# a.waitForArduino("{") # Arduino is ready! 
	# 	# a.initiateWithArduino(mm)
	# 	# while 1==1:
	# 	# 	a.communicateWithArduino(mm)

    endpoints_to_steps_server()

    #4.0494 eucentric