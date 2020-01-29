import time

import matplotlib.pyplot as plt
import modules.stepMath as smath

def getSteps(motorList):
        # step angle in radians
    stepAngle = smath.stepAngle
    start = time.perf_counter()

    for m in motorList:
        #m.listSteps()
        #plt.scatter(m.timeList, m.stepList, label=f"{m.motorIndex}")

        m.dictSteps()
        #plt.scatter(list(m.stepDict.keys()), list(m.stepDict.values()), label=f"{m.motorIndex}")       

    # end = time.perf_counter()
    # print(f"dictionary route: {end-start}")
    plt.show() 
    

