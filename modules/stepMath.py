import numpy as np

def nearestStep(value):
    if value%stepAngle < stepAngle/2:
        return value//stepAngle*stepAngle
    else:
        return (value//stepAngle + 1)*stepAngle

def ceilStep(value):
    return (value//stepAngle + 1)*stepAngle

def floorStep(value):
    return value//stepAngle*stepAngle

# max frameTime is 100ms because that is the cutoff in the bytes I send to Arduino only 0-100
# can change frameTime to 60, 61-64 reserved for ArduinoStartBytes, and the last 2 bits used for direction
frameTime = 0.06

# which single step angle being used, 1.8 for standard, 0.9 for half stepping(i need to change the Seq in Arduino if I change this)
stepAngle = 1.8 *np.pi/180 / 4

# speed of the endPoint
speed = 1 #in/s
