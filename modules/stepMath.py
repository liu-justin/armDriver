def nearestStep(value, step):
    if value%step < step/2:
        return value//step*step
    else:
        return (value//step + 1)*step

def ceilStep(value, step):
    return (value//step + 1)*step

def floorStep(value, step):
    return value//step*step

frameTime = 0.1