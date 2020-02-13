import numpy as np

# max frameTime is 100ms because that is the cutoff in the bytes I send to Arduino only 0-100
# can change frameTime to 60, 61-64 reserved for ArduinoStartBytes, and the last 2 bits used for direction
frameTime = 0.06

# which single step angle being used, 1.8 for standard, 0.9 for half stepping(i need to change the Seq in Arduino if I change this)
stepAngle = 1.8 *np.pi/180 / 4
# stepAngle = 0.01

# speed of the endPoint
speed = 1 #in/s

def nearestStep(value):
    if value%stepAngle < stepAngle/2:
        return value//stepAngle*stepAngle
    else:
        return (value//stepAngle + 1)*stepAngle

def ceilStep(value):
    return (value//stepAngle + 1)*stepAngle

def floorStep(value):
    return value//stepAngle*stepAngle

def ceilHalfStep(value):
    return (value-(stepAngle/2))//stepAngle*stepAngle + 3*stepAngle/2

def floorHalfStep(value):
    return (value-(stepAngle/2))//stepAngle*stepAngle + stepAngle/2

def calcStepsInFrame(frameCurrent, frameNext):
	frameMin = min(frameCurrent, frameNext)
	return int(abs(frameNext//stepAngle - frameCurrent//stepAngle)) + (1 if frameMin%stepAngle == 0 else 0)

def calcHalfStepsInFrame(frameCurrent, frameNext):
	frameMin = min(frameCurrent, frameNext)
	return int(round(abs(floorHalfStep(frameNext) - floorHalfStep(frameCurrent))/stepAngle)) + (1 if (frameCurrent-stepAngle/2)%stepAngle == 0 else 0)

# stepsInFrame = int(abs(frameNext//smath.stepAngle - frameCurrent//smath.stepAngle)) + (1 if frameMin%smath.stepAngle == 0 else 0)
# print(round((floorHalfStep(2.3291313354487455) - floorHalfStep(2.3241447965846715))/stepAngle))