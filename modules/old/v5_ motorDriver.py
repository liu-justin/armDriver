import time
import numpy as np
import math

import matplotlib.pyplot as plt

import modules.pointFinder as p

Seq = []
Seq.append([1,0,1,0])
Seq.append([0,1,1,0])
Seq.append([0,1,0,1])
Seq.append([1,0,0,1])

class Motor:
    def __init__(self, anglesIndex):
        _i = anglesIndex
        timeIter = 0
        timeList = [timeIter]
        stepIter = ceilStep(angles[0][_i], stepAngle) if (angles[1][_i] - angles[0][_i] < 0) else floorStep(angles[0][_i], stepAngle)
        stepList = [stepIter]

def nearestStep(value, step):
    if value%step < step/2:
        return value//step*step
    else:
        return (value//step + 1)*step

def ceilStep(value, step):
    return (value//step + 1)*step

def floorStep(value, step):
    return value//step*step

def getSteps(angles):

    frameTime = p.frameTime
        # step angle in radians
    stepAngle = 1.8 *np.pi/180

    R0 = Motor(0)
    RA = Motor(1)
    N17 = Motor(2)
    Theta = Motor(3)

    stepIterR = ceilStep(angles[0][0], stepAngle) if (angles[1][0] - angles[0][0] < 0) else floorStep(angles[0][0], stepAngle)
    stepIterC = ceilStep(angles[0][1], stepAngle) if (angles[1][1] - angles[0][1] < 0) else floorStep(angles[0][1], stepAngle)
    stepListR = [stepIterR]
    stepListC = [stepIterC]
    
    for i in range(len(angles)-1):

        # get the total angle to travel during the frame for both linkage R and C
        angleR1 = angles[i+1][0]
        angleR0 = angles[i][0]
        angleRmin = min(angleR1, angleR0)
        angleC1 = angles[i+1][1]
        angleC0 = angles[i][1]
        angleCmin = min(angleC1, angleC0)

        # # counts the number of motor steps (1.8 degrees) that are in the frame, by subtracting the upper number of steps and the lower number of steps
        # # the end case is if the lower number of steps is an actual multiple, which should be impossible with floats but just an if
        stepCountR = int(abs(angleR1//stepAngle - angleR0//stepAngle) + (1 if angleRmin%stepAngle == 0 else 0))
        stepCountC = int(abs(angleC1//stepAngle - angleC0//stepAngle) + (1 if angleCmin%stepAngle == 0 else 0))

        # if there is no steps between R1 and R0, then do nothing, otherwise
        if stepCountR > 0:
            # find and append the first step: 
            # if the slope is positive, find the next step above angleR0; opposite for slope is negative
            stepIterR = ceilStep(angleR0, stepAngle) if (angleR1 - angleR0 > 0) else floorStep(angleR0, stepAngle)
            stepListR.append(stepIterR)
            # find the first time with linear interpolation
            firstT = (stepListR[-1] - angleR0)/(angleR1 - angleR0) * frameTime + i*frameTime
            timeListR.append(firstT)

            for j in range(1, stepCountR):
                stepListR.append(stepListR[-1]+stepAngle*np.sign(angleR1-angleR0))
                t = (stepListR[-1] - angleR0)/(angleR1 - angleR0) * frameTime + i*frameTime
                timeListR.append(t)
        else:
            stepListR.append(nearestStep(angleR0, stepAngle))
            timeListR.append(i*frameTime)


        if stepCountC > 0:
            stepIterC = ceilStep(angleC0, stepAngle) if (angleC1 - angleC0 > 0) else floorStep(angleC0, stepAngle)
            stepListC.append(stepIterC)
            firstT = (stepListC[-1] - angleC0)/(angleC1 - angleC0) * frameTime + i*frameTime # adding the time is wrong
            timeListC.append(firstT)
            
            for j in range(1, stepCountC):
                stepListC.append(stepListC[-1]+stepAngle*np.sign(angleC1-angleC0))
                t = (stepListC[-1] - angleC0)/(angleC1 - angleC0) * frameTime + i*frameTime
                timeListC.append(t)
        else:
            stepListC.append(nearestStep(angleC0, stepAngle))
            timeListC.append(i*frameTime)


    # correcting the very first angles to be as close to real as possible
    stepListR[0] = nearestStep(angles[0][0], stepAngle)
    stepListC[0] = nearestStep(angles[0][1], stepAngle)

    # adding the last step position and the last time, based on rounding to the nearest step
    stepListR.append(nearestStep(angles[-1][0], stepAngle))
    stepListC.append(nearestStep(angles[-1][1], stepAngle))
    timeListR.append(frameTime*(len(angles)-1))
    timeListC.append(frameTime*(len(angles)-1))

    plt.scatter(timeListC, stepListC, label="angleC steps")
    plt.scatter(timeListR, stepListR, label="angleR steps")
    # for i, txt in enumerate(stepListC):
    #     plt.annotate(i, (timeListC[i], stepListC[i]))

    print(f"R: {len(timeListR)}")
    print(f"C: {len(timeListC)}")

    #plt.show() 

    return timeListR, stepListR, timeListC, stepListC; 

    

