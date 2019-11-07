import time
import numpy as np
import math

import matplotlib.pyplot as plt
import modules.stepMath as smath

def getSteps(motorList):

    frameTime = smath.frameTime
        # step angle in radians
    stepAngle = 1.8 *np.pi/180
    
    for i in range(len(motorList[0].frameList)-1):

        for m in motorList:
            frameCurrent = m.frameList[i]
            frameNext = m.frameList[i+1]
            frameMin = min(frameCurrent, frameNext)
            # counts the number of motor steps (1.8 degrees) that are in the frame, by subtracting the upper number of steps and the lower number of steps
            # the end case is if the lower number of steps is an actual multiple, which should be impossible with floats but just an if
            stepsInFrame = int(abs(frameNext//stepAngle - frameCurrent//stepAngle)) + (1 if frameMin%stepAngle == 0 else 0)

            if stepsInFrame > 0:
                stepIter = smath.ceilStep(frameCurrent, stepAngle) if (frameNext - frameCurrent > 0) else smath.floorStep(frameCurrent, stepAngle)
                m.stepList.append(stepIter)
                firstT = (m.stepList[-1] - frameCurrent)/(frameNext - frameCurrent) * frameTime + i*frameTime
                m.timeList.append(firstT)

                for j in range(1, stepsInFrame):
                    m.stepList.append(m.stepList[-1] + stepAngle*np.sign(frameNext - frameCurrent))
                    t = (m.stepList[-1] - frameCurrent)/(frameNext - frameCurrent) * frameTime + i*frameTime
                    m.timeList.append(t)
            else:
                m.stepList.append(smath.nearestStep(frameCurrent, stepAngle))
                m.timeList.append(i*frameTime)

    for m in motorList:
        # adding the last step position and the last time, based on rounding to the nearest step
        m.stepList[0] = smath.nearestStep(m.frameList[0], stepAngle)
        m.stepList.append(smath.nearestStep(m.frameList[-1], stepAngle))
        m.timeList.append(frameTime*(len(m.frameList)-1))

        plt.scatter(m.timeList, m.stepList, label=f"{m.motorIndex}")

    plt.show() 
    

