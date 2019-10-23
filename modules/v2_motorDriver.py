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

def getSteps(angles):

    frameTime = 0.125

    # for graphing purposes only
    timeListR = []
    timeListC = []
    tIterR = 0
    tIterC = 0

    stepListR = []
    stepListC = []
    stepIterR = angles[0][0]
    stepIterC = angles[0][1]

    # use enumerate and this weird unpacking tuple to get an index and value
    #for idx, (angleR, angleC) in enumerate(angles):
    for i in range(len(angles)-1):
        # get the total angle to travel

        frameAngleR = angles[i+1][0] - angles[i][0]
        frameAngleC = angles[i+1][1] - angles[i][1]

        # step angle in radians
        stepAngle = 1.8 *np.pi/180

        # steps can negative, need to fix
        stepCountR = int(round(frameAngleR/stepAngle))
        stepCountC = int(round(frameAngleC/stepAngle))

        print(f"R: {stepCountR} C: {stepCountC}")
        if stepCountR == 0:
            stepTimeR = frameTime
            timeListR.append(tIterR)
            stepListR.append(stepIterR)
            tIterR += stepTimeR
            print(f"delayR: {stepTimeR} TimeR: {tIterR}")
        else:
            stepTimeR = abs(frameTime/stepCountR)
            for i in range(0,abs(stepCountR)):
                timeListR.append(tIterR)
                stepListR.append(stepIterR)
                tIterR += stepTimeR
                stepIterR += np.sign(stepCountR)*stepAngle
                print(f"delayR: {stepTimeR} TimeR: {tIterR}")

        if stepCountC == 0:
            stepTimeC = frameTime
            timeListC.append(tIterC)
            stepListC.append(stepIterC)
            tIterC += stepTimeC
            print(f"delayC: {stepTimeC} TimeC: {tIterC} ")
        else:
            stepTimeC = abs(frameTime/stepCountC)
            for i in range(0,abs(stepCountC)):
                timeListC.append(tIterC)
                stepListC.append(stepIterC)
                tIterC += stepTimeC
                stepIterC += np.sign(stepCountC)*stepAngle
                print(f"delayC: {stepTimeC} TimeC: {tIterC} ")

        # if angle is clockwise, check the wiring
        # if (frameAngleR > 0):
        #     R0.forward(stepTimeR, stepCountR)
        # else:
        #     R0.backward(stepTimeR, stepCountR)

        # if (frameAngleC > 0):
        #     RA.forward(stepTimeC, stepCountC)
        # else:
        #     RA.backward(stepTimeC, stepCountC)
    timeListR.append(tIterR)
    stepListR.append(stepIterR)
    timeListC.append(tIterC)
    stepListC.append(stepIterC)

    plt.step(timeListC, stepListC, where="mid", label="angleC steps")
    plt.step(timeListR, stepListR, where="mid", label="angleR steps")
    plt.xlabel("time (secs)")
    plt.ylabel("angle from east (radians)")
    plt.legend()
    plt.show() 

