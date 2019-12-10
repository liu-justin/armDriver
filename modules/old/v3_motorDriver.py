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

def getSteps(angles):

    frameTime = 0.1
        # step angle in radians
    stepAngle = 1.8 *np.pi/180

    # for graphing purposes only
    tIterR = 0
    tIterC = 0
    timeListR = [tIterR]
    timeListC = [tIterC]
    
    stepIterR = nearestStep(angles[0][0], stepAngle)
    stepIterC = angles[0][1]
    stepListR = [stepIterR]
    stepListC = [stepIterC]
    
    # use enumerate and this weird unpacking tuple to get an index and value
    #for idx, (angleR, angleC) in enumerate(angles):
    for i in range(len(angles)-1):

        # # get the total angle to travel during the frame for both linkage R and C
        angleR1 = angles[i+1][0]
        angleR0 = angles[i][0]
        angleC1 = angles[i+1][1]
        angleC0 = angles[i][1]

        # # counts the number of motor steps (1.8 degrees) that are in the frame, by subtracting the upper number of steps and the lower number of steps
        # # the end case is if the lower number of steps is an actual multiple, which should be impossible with floats but just an if
        stepCountR = int(abs(angleR1//stepAngle - angleR0//stepAngle) + (1 if angleR0%stepAngle == 0 else 0))
        stepCountC = int(abs(angleC1//stepAngle - angleC0//stepAngle) + (1 if angleC0%stepAngle == 0 else 0))

        print(f"stepCountR: {stepCountR} stepCountC: {stepCountC}")

        # next steps are to find what step multiples are inside the two angles, and then linearly interpolate them
        # finding the first step from angleR0
        if stepCountR == 0:
            x  = 0
        else:
            firstStep = angleR0//stepAngle*stepAngle + (0 if i%stepAngle==0 else stepAngle*np.sign(angleR1-angleR0))
            stepListR.append(firstStep)
            firstT = (stepListR[-1] - angleR0)/(angleR1 - angleR0) * frameTime + timeListR[-1]
            timeListR.append(firstT)
            print(f" before the for loop, and after the first: {[i/stepAngle for i in stepListR]}")
            

            for i in range(1, stepCountR):
                stepListR.append(stepListR[-1]+stepAngle*np.sign(angleR1-angleR0))
                t = (stepListR[-1] - angleR0)/(angleR1 - angleR0) * frameTime + timeListR[-1-i]
                print(f"sign of t: {np.sign((stepListR[-1] - angleR0)/(angleR1 - angleR0))}")
                timeListR.append(t)

            print([i/stepAngle for i in stepListR])
            print(timeListR)

        # if stepCountC == 0:
        #     stepTimeC = frameTime
        #     tIterC += stepTimeC
        #     timeListC.append(tIterC)
        #     stepListC.append(stepIterC)
        # else:
        #     stepTimeC = abs(frameTime/stepCountC)
        #     for i in range(0,abs(stepCountC)):
        #         tIterC += stepTimeC
        #         stepIterC += np.sign(stepCountC)*stepAngle
        #         timeListC.append(tIterC)
        #         stepListC.append(stepIterC)

    # timeListR.append(tIterR)
    # stepListR.append(stepIterR)
    # timeListC.append(tIterC)
    # stepListC.append(stepIterC)

    #plt.step(timeListC, stepListC, where="mid", label="angleC steps")
    #plt.step(timeListR, stepListR, where="post", label="angleR steps")
    plt.scatter(timeListR, stepListR, label="angleR steps")

    plt.show() 

