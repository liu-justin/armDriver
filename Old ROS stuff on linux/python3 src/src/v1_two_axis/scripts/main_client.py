#!/usr/bin/env python

import sys
import rospy
from v1_3axis.srv import *
import pointFinder as p
import stepFinder as s
import Motor
import MotorList

def endpoints_to_steps_client(startX, startY, endX, endY):
    rospy.wait_for_service('endpoints_to_steps')
    try:
        endpoints_to_steps = rospy.ServiceProxy('endpoints_to_steps', EndpointsToSteps)
        resp1 = endpoints_to_steps(startX, startY, endX, endY)
        print(resp1.R0Steps)
        print(resp1.RASteps)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [startX startY endX endY]"%sys.argv[0]

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 5:
        startX = float(sys.argv[1])
        startY = float(sys.argv[2])
        #startPoint = p.Point(startX, startY)
        endX = float(sys.argv[3])
        endY = float(sys.argv[4])
        #endPoint = p.Point(endX, endY)
    else:
        print usage()
        sys.exit(1)
    #print "startPoint: %s, endPoint: %s"%(startPoint,endPoint)
    endpoints_to_steps_client(startX, startY, endX, endY)

    