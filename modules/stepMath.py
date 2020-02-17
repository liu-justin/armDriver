import numpy as np
import time

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

def calcZeroSteps(time):
	return time//int(frameTime*1000)

def calcRoundedTime(k, zeroSteps, deltaT):
	return int(round(deltaT*(k+1)/(zeroSteps+1)))

def calcSplitTimes(time, stepTuple):
	divisor = int(time//(frameTime*1000))
	rounded = time//(divisor+1)
	remainder = time%(divisor+1)
	for i in range(0,divisor):
		stepTuple.append((stepTuple[-1][0]+rounded+np.sign(remainder).item(), stepTuple[-1][1], rounded+np.sign(remainder).item(), 121))
		remainder -= np.sign(remainder).item()

def calcSplitTimesInt(time, stepTuple):
	divisor = int(time//(frameTime*1000))
	rounded = time//(divisor+1)
	remainder = time%(divisor+1)
	#print(rounded, remainder)
	for i in range(0,divisor):
		stepTuple.append((stepTuple[-1][0]+rounded+int(np.sign(remainder)), stepTuple[-1][1], rounded+int(np.sign(remainder)), 121))
		remainder -= int(np.sign(remainder))

def calcSplitTimesIntBool(time, stepTuple):
	divisor = int(time//(frameTime*1000))
	rounded = time//(divisor+1)
	remainder = time%(divisor+1)
	#print(rounded, remainder)
	for i in range(0,divisor):
		stepTuple.append((stepTuple[-1][0]+rounded+int(bool(remainder)), stepTuple[-1][1], rounded+int(bool(remainder)), 121))
		remainder -= int(bool(remainder))

def calcSplitTimesIfElse(time, stepTuple):
	divisor = int(time//(frameTime*1000))
	rounded = time//(divisor+1)
	remainder = time%(divisor+1)
	#print(rounded, remainder)
	for i in range(0,divisor):
		stepTuple.append((stepTuple[-1][0]+ rounded + (0 if remainder <= 0 else 1), stepTuple[-1][1], rounded + (0 if remainder <= 0 else 1), 121))
		remainder -= 1

# stepTuple = [(0,0.1245333), (0.039353591123, 0.1245669, 10, 121)]
# deltaT = 185

# startB = time.perf_counter()
# zeroSteps = calcZeroSteps(deltaT)
# previousRoundedTime = 0
# for k in range(0,zeroSteps):
#     roundedTime = int(round(deltaT*(k+1)/(zeroSteps+1)))
#     stepTuple.append((stepTuple[-1-k][0]+roundedTime/1000, stepTuple[-1][1], roundedTime-previousRoundedTime, 121))
#     previousRoundedTime = roundedTime
# endB = time.perf_counter()
# print(f"timeB: {endB - startB}")
# print(stepTuple)

# stepTuple = [(0,0.1245333), (0.039353591123, 0.1245669, 10, 121)]
# startA = time.perf_counter()
# calcSplitTimes(deltaT,stepTuple)
# endA = time.perf_counter()
# print(f"timeA: {endA-startA}")
# print(stepTuple)

# stepTuple = [(0,0.1245333), (0.039353591123, 0.1245669, 10, 121)]
# startAI = time.perf_counter()
# calcSplitTimesInt(deltaT,stepTuple)
# endAI = time.perf_counter()
# print(f"timeAI: {endAI-startAI}")
# print(stepTuple)

# stepTuple = [(0,0.1245333), (0.039353591123, 0.1245669, 10, 121)]
# startAIB = time.perf_counter()
# calcSplitTimesIntBool(deltaT,stepTuple)
# endAIB = time.perf_counter()
# print(f"timeAIB: {endAIB-startAIB}")
# print(stepTuple)

# stepTuple = [(0,0.1245333), (0.039353591123, 0.1245669, 10, 121)]
# startAIf = time.perf_counter()
# calcSplitTimesIfElse(deltaT,stepTuple)
# endAIf = time.perf_counter()
# print(f"timeAIf: {endAIf-startAIf}")
# print(stepTuple)

# def splitTime(x):
# 	divisor = x//50+1
# 	exact = x/divisor
# 	roundedFract = x%divisor
# 	return(x, divisor, exact, roundedFract, math.ceil(exact)*(roundedFract)+math.floor(exact)*(divisor - roundedFract))

# stepsInFrame = int(abs(frameNext//smath.stepAngle - frameCurrent//smath.stepAngle)) + (1 if frameMin%smath.stepAngle == 0 else 0)
# print(round((floorHalfStep(2.3291313354487455) - floorHalfStep(2.3241447965846715))/stepAngle))

#was inside motor.tupleStepsHalfwayBtwnChange
# if (smath.calcDivisorForMultiples(deltaT)>1):
#     divisor = smath.calcDivisorForMultiples(deltaT)
#     print(f"deltaT is greater than 60: {deltaT}, divisor is: {divisor} the stepTuple: {self.stepTuple}")
#     for k in range(0, deltaT%divisor):
#         self.stepTuple.append((self.stepTuple[-1][0]+math.ceil(deltaT/divisor)/1000, self.stepTuple[-1][1], math.ceil(deltaT/divisor), 121))
#     print(f"after the first one {self.stepTuple}")
#     for k in range(deltaT%divisor, divisor-deltaT%divisor-1):
#         self.stepTuple.append((self.stepTuple[-1][0]+math.floor(deltaT/divisor)/1000, self.stepTuple[-1][1], math.floor(deltaT/divisor), 121))                            
#     print(f"after the second one {self.stepTuple}")