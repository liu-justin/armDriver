import modules.stepMath as smath
import numpy as np

class Motor:
    def __init__(self, motorIndex):
        self._mi = motorIndex
        # Arduino start reading bytes start at R0 motor, byte 103
        self.arduinoStartByte = motorIndex + 105
        self.frameList = []
        self.timeList = []
        self.stepList = []
        self.stepDict = {}
        
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
        
    @property
    def motorIndex(self):
        return self._mi
