import stepMath as smath

def getSteps(motorList):
        # step angle in radians
    #start = time.perf_counter()

    for m in motorList:
        #m.listSteps()
        #plt.scatter(m.timeList, m.stepList, label=f"{m.motorIndex}")

        # m.tupleSteps()
        # plt.scatter([elem[0] for elem in m.stepTuple], [elem[1] for elem in m.stepTuple], label=f"Motor {m.motorIndex} tupleList")
        
        m.tupleStepsHalfwayBtwnChange()
        #plt.scatter([elem[0] for elem in m.stepTuple], [elem[1] for elem in m.stepTuple], label=f"Motor {m.motorIndex} tupleList half")
        
        #m.dictSteps()
        # plt.scatter(list(m.stepDict.keys()), list(m.stepDict.values()), label=f"{m.motorIndex}")       

    # end = time.perf_counter()
    # print(f"dictionary route: {end-start}")