#import RPi.GPIO as GPIO
import time

import numpy as np
import math

import matplotlib.pyplot as plt

power_pin = 18
button_pin = 27

Seq = []
Seq.append([1,0,1,0])
Seq.append([0,1,1,0])
Seq.append([0,1,0,1])
Seq.append([1,0,0,1])

class Motor:
    def __init__(self, a1, a2, b1, b2):
        self.a1 = a1
        self.a2 = a2
        self.b1 = b1
        self.b2 = b2
        self.stepCounter = 0

    def setStep(self, w):
        #GPIO.output(coilA1Pin, w[0])
        #GPIO.output(coilA2Pin, w[1])
        #GPIO.output(coilB1Pin, w[2])
        #GPIO.output(coilB2Pin, w[3])
        #print("setting step")
        x = 1

    def forward(self, delay, steps):
        for i in range(steps):
            self.stepCounter += 1
            self.setStep(Seq[self.stepCounter%4])
            #time.sleep(delay)

    def backward(self, delay, steps):
        for i in range(steps):
            self.stepCounter -= 1
            self.setStep(Seq[self.stepCounter%4])
            #time.sleep(delay)

R0 = Motor(4, 17, 23, 24)
RA = Motor(4, 17, 23, 24)
N17 = Motor(4, 17, 23, 24)
Theta = Motor(4, 17, 23, 24)

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

    frameTime = 0.1
        # step angle in radians
    stepAngle = 1.8 *np.pi/180

    # for graphing purposes only
    tIterR = 0
    tIterC = 0
    timeListR = [tIterR]
    timeListC = [tIterC]

    stepIterR = ceilStep(angles[0][0], stepAngle) if (angles[1][0] - angles[0][0] < 0) else floorStep(angles[0][0], stepAngle)
    stepIterC = ceilStep(angles[0][1], stepAngle) if (angles[1][1] - angles[0][1] < 0) else floorStep(angles[0][1], stepAngle)
    stepListR = [stepIterR]
    stepListC = [stepIterC]
    
    for i in range(len(angles)-1):

        # get the total angle to travel during the frame for both linkage R and C
        angleR1 = angles[i+1][0]
        angleR0 = angles[i][0]
        angleC1 = angles[i+1][1]
        angleC0 = angles[i][1]

        # # counts the number of motor steps (1.8 degrees) that are in the frame, by subtracting the upper number of steps and the lower number of steps
        # # the end case is if the lower number of steps is an actual multiple, which should be impossible with floats but just an if
        stepCountR = int(abs(angleR1//stepAngle - angleR0//stepAngle) + (1 if angleR0%stepAngle == 0 else 0))
        stepCountC = int(abs(angleC1//stepAngle - angleC0//stepAngle) + (1 if angleC0%stepAngle == 0 else 0))

        # if there is no steps between R1 and R0, then do nothing
        if stepCountR > 0:
            # find the first step
            stepIterR = ceilStep(angleR0, stepAngle) if (angleR1 - angleR0 > 0) else floorStep(angleR0, stepAngle)
            stepListR.append(stepIterR)
            firstT = (stepListR[-1] - angleR0)/(angleR1 - angleR0) * frameTime + i*frameTime
            timeListR.append(firstT)

            for j in range(1, stepCountR):
                stepListR.append(stepListR[-1]+stepAngle*np.sign(angleR1-angleR0))
                t = (stepListR[-1] - angleR0)/(angleR1 - angleR0) * frameTime + i*frameTime
                timeListR.append(t)

        if stepCountC > 0:
            stepIterC = ceilStep(angleC0, stepAngle) if (angleC1 - angleC0 > 0) else floorStep(angleC0, stepAngle)
            stepListC.append(stepIterC)
            firstT = (stepListC[-1] - angleC0)/(angleC1 - angleC0) * frameTime + i*frameTime # adding the time is wrong
            timeListC.append(firstT)
            
            for j in range(1, stepCountC):
                stepListC.append(stepListC[-1]+stepAngle*np.sign(angleC1-angleC0))
                t = (stepListC[-1] - angleC0)/(angleC1 - angleC0) * frameTime + i*frameTime
                timeListC.append(t)

    print(timeListR)
    plt.step(timeListC, stepListC, where="mid", label="angleC steps")
    plt.step(timeListR, stepListR, where="mid", label="angleR steps")
    # for i, txt in enumerate(stepListC):
    #     plt.annotate(i, (timeListC[i], stepListC[i]))

    plt.show() 

