import modules.stepMath as smath
import numpy as np
import math

class Motor:
    def __init__(self, motorList):
        motorList.append(self)
        self._motorIndex = len(motorList)-1
        # Arduino start reading bytes start at R0 motor, byte 103
        self.arduinoStartByte = self._motorIndex + 105
        self.frameList = []
        self.timeList = []
        self.stepList = []
        self.stepTuple = [] #(time, step, time from last time, step from last step)
        self.tupleCounter = 0
        self.stepDict = {}

        # 1:ready, 2:moving, 3:not homed 4: error
        self.state = 3
        
    def listSteps(self):
        self.timeList.append(0)
        angleNext = self.frameList[1]
        angleCurrent = self.frameList[0]
        stepIter = smath.ceilStep(angleCurrent) if (angleNext - angleCurrent < 0) else smath.floorStep(angleCurrent)
        self.stepList.append(stepIter)

        for i in range(len(self.frameList)-1):
            frameCurrent = self.frameList[i]
            frameNext = self.frameList[i+1]
            frameMin = min(frameCurrent, frameNext)
            # counts the number of motor steps (1.8 degrees) that are in the frame, by subtracting the upper number of steps and the lower number of steps
            # the end case is if the lower number of steps is an actual multiple, which should be impossible with floats but just an if
            stepsInFrame = int(abs(frameNext//smath.stepAngle - frameCurrent//smath.stepAngle)) + (1 if frameMin%smath.stepAngle == 0 else 0)

            if stepsInFrame > 0:
                stepIter = smath.ceilStep(frameCurrent) if (frameNext - frameCurrent > 0) else smath.floorStep(frameCurrent)
                self.stepList.append(stepIter)
                firstT = (stepIter - frameCurrent)/(frameNext - frameCurrent) * smath.frameTime + i*smath.frameTime
                self.timeList.append(firstT)

                for j in range(1, stepsInFrame):
                    self.stepList.append(self.stepList[-1] + smath.stepAngle*np.sign(frameNext - frameCurrent))
                    t = (self.stepList[-1] - frameCurrent)/(frameNext - frameCurrent) * smath.frameTime + i*smath.frameTime
                    self.timeList.append(t)
            else:
                self.stepList.append(smath.nearestStep(frameCurrent))
                self.timeList.append(i*smath.frameTime)

        self.stepList[0] = smath.nearestStep(self.frameList[0])
        self.stepList.append(smath.nearestStep(self.frameList[-1]))
        self.timeList.append(smath.frameTime*(len(self.frameList)-1))

    def tupleSteps(self):
        angleNext = self.frameList[1]
        angleCurrent = self.frameList[0]
        stepIter = smath.ceilStep(angleCurrent) if (angleNext - angleCurrent < 0) else smath.floorStep(angleCurrent)
        self.stepTuple.append((0,stepIter))
        #print(f"First tuple: {self.stepTuple}")

        for i in range(len(self.frameList)-1):
            frameCurrent = self.frameList[i]
            frameNext = self.frameList[i+1]
            # counts the number of motor steps (1.8 degrees) that are in the frame, by subtracting the upper number of steps and the lower number of steps
            # the end case is if the lower number of steps is an actual multiple, which should be impossible with floats but just an if
            stepsInFrame = smath.calcStepsInFrame(frameCurrent, frameNext)

            if stepsInFrame > 0:
                stepIter = smath.ceilStep(frameCurrent) if (frameNext - frameCurrent > 0) else smath.floorStep(frameCurrent)
                firstT = (stepIter - frameCurrent)/(frameNext - frameCurrent) * smath.frameTime + i*smath.frameTime
                deltaT = int(round(1000*(firstT - self.stepTuple[-1][0])))
                deltaS = int(np.sign(stepIter - self.stepTuple[-1][1])) + 121
                self.stepTuple.append((firstT, stepIter, deltaT, deltaS))
                #print(f"If stepsInFrame is > 0, then this is the first tuple: {self.stepTuple}")

                # if there are any intersection points in the current frameTime, then grab them here
                for j in range(1, stepsInFrame):
                    s = self.stepTuple[-1][1] + smath.stepAngle*np.sign(frameNext - frameCurrent)
                    t = (s - frameCurrent)/(frameNext - frameCurrent) * smath.frameTime + i*smath.frameTime
                    deltaT = int(round(1000*(t - self.stepTuple[-1][0])))
                    deltaS = int(np.sign(s - self.stepTuple[-1][1])) + 121
                    self.stepTuple.append((t,s, deltaT, deltaS))
                    #print(f"This is the {j} tuple: {self.stepTuple}")
            
            s = smath.nearestStep(frameNext)
            t = (i+1)*smath.frameTime
            deltaT = int(round(1000*(t - self.stepTuple[-1][0])))
            deltaS = int(np.sign(s - self.stepTuple[-1][1])) + 121
            self.stepTuple.append((t,s, deltaT, deltaS))

        self.stepTuple[0] = (0,smath.nearestStep(self.frameList[0]))
        s = smath.nearestStep(self.frameList[-1])
        t = smath.frameTime*(len(self.frameList)-1)
        deltaT = int(round(1000*(t - self.stepTuple[-1][0])))
        deltaS = int(np.sign(s - self.stepTuple[-1][1])) + 121
        self.stepTuple.append((t,s, deltaT, deltaS))
        #print(f" last step: {self.stepTuple}")

    def tupleStepsHalfwayBtwnChange(self):
        # appends the first step to the tupleStep list, deltaT is 0, and direction is 0
        stepIter = smath.nearestStep(self.frameList[0])
        self.stepTuple.append((0,stepIter,0,121))

        for i in range(len(self.frameList)-1):
            frameCurrent = self.frameList[i]
            frameNext = self.frameList[i+1]
            # counts number of half steps between steps, doesnt include the whole steps, only half steps
            stepsInFrame = smath.calcHalfStepsInFrame(frameCurrent, frameNext)
            #print(f"i: {i} frameCurrent: {frameCurrent} frameNext: {frameNext} stepsInFrame: {stepsInFrame}")

            if stepsInFrame > 0:

                # if there are any intersection points in the current frameTime, then grab them here
                for j in range(0, stepsInFrame):
                    s = self.stepTuple[-1][1] + smath.stepAngle*np.sign(frameNext - frameCurrent)
                    t = ((self.stepTuple[-1][1] + s)/2 - frameCurrent)/(frameNext - frameCurrent) * smath.frameTime + i*smath.frameTime
                    deltaT = int(round(1000*(t - self.stepTuple[-1][0])))
                    deltaS = int(np.sign(s - self.stepTuple[-1][1])) + 121 # maybe np.sign(frameNext - frameCurrent)
                    #print(f"s: {s} previousStepTuple: {self.stepTuple[-1][1]} halfway point: {((self.stepTuple[-1][1] + s)/2)} frameCurrent: {(frameCurrent)} frameNext: {frameNext}")
                    
                    # want to keep steps under a set number(frame length*1000),
                    # so any deltaT that are greater than that set number is going to get cut down as evenly as possible
                    self.appendFillerSteps(t,s,deltaT, deltaS)

        s = smath.nearestStep(self.frameList[-1])
        t = smath.frameTime*(len(self.frameList)-1)
        deltaT = int(round(1000*(t - self.stepTuple[-1][0])))
        deltaS = int(np.sign(s - self.stepTuple[-1][1])) + 121
        self.appendFillerSteps(t,s,deltaT, deltaS)
        #print(f" last step: {self.stepTuple}")

    def appendFillerSteps(self,t,s,deltaT, deltaS):

        divisor = int(deltaT//(smath.frameTime*1000))
        rounded = deltaT//(divisor+1)
        remainder = deltaT%(divisor+1)
        #print(rounded, remainder)
        for i in range(0,divisor):
            self.stepTuple.append((self.stepTuple[-1][0]+ rounded/1000 + (0 if remainder <= 0 else 0.001), self.stepTuple[-1][1], rounded + (0 if remainder <= 0 else 1), 121))
            remainder -= 1
        self.stepTuple.append((t, s, rounded, deltaS))
            #print(self.stepTuple)

    def dictSteps(self):

        # initialization for the first step of stepDict
        frame1 = self.frameList[1]
        frame0 = self.frameList[0]
        #ceilStep(angles[0][_i], smath.stepAngle) if (angles[1][_i] - angles[0][_i] < 0) else floorStep(angles[0][_i], smath.stepAngle)
        step0 = smath.ceilStep(frame0) if (frame1 - frame0 < 0) else smath.floorStep(frame0)
        self.stepDict[0] = step0

        for i in range(len(self.frameList)-1):
            frameCurrent = self.frameList[i]
            frameNext = self.frameList[i+1]
            frameMin = min(frameCurrent, frameNext)
            stepsInFrame = int(abs(frameNext//smath.stepAngle - frameCurrent//smath.stepAngle)) + (1 if frameMin%smath.stepAngle == 0 else 0)

            if stepsInFrame > 0:
                stepBefore = smath.ceilStep(frameCurrent) if (frameNext - frameCurrent > 0) else smath.floorStep(frameCurrent)
                firstT = (stepBefore - frameCurrent)/(frameNext - frameCurrent) * smath.frameTime + i*smath.frameTime
                self.stepDict[firstT] = stepBefore

                for j in range(1, stepsInFrame):
                    stepIter = stepBefore + smath.stepAngle*np.sign(frameNext - frameCurrent)
                    t = (stepIter - frameCurrent)/(frameNext - frameCurrent) * smath.frameTime + i*smath.frameTime
                    self.stepDict[t] = stepIter
                    stepBefore = stepIter
            else:
                self.stepDict[i*smath.frameTime] = smath.nearestStep(frameCurrent)
                self.stepDict[(i+1)*smath.frameTime] = smath.nearestStep(frameNext)

        self.stepDict[0] = smath.nearestStep(self.frameList[0])
        self.stepDict[smath.frameTime*(len(self.frameList)-1)] = smath.nearestStep(self.frameList[-1])

        print(self.stepDict)
        print(len(self.stepDict))

    @property
    def motorIndex(self):
        return self._motorIndex

    @motorIndex.setter
    def motorIndex(self, mi):
        _motorIndex = mi
