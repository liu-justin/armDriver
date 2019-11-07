class Motor:
    def __init__(self, motorIndex):
        self._mi = motorIndex
        self.frameList = []
        self.timeList = [0]
        self.stepIter = 0#ceilStep(angles[0][_i], stepAngle) if (angles[1][_i] - angles[0][_i] < 0) else floorStep(angles[0][_i], stepAngle)
        self.stepList = [self.stepIter]


    def startStepList():
        angleNext = self.frameList[1]
        angleCurrent = self.frameList[0]
        

    @property
    def motorIndex(self):
        return self._mi
