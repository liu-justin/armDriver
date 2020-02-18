class MotorManager:
    def __init__(self):
        # Arduino start reading bytes start at R0 motor, byte 103
        self.motorList = []

    def append(self, motor):
        self.motorList.append(motor)

    def __len__(self):
        return len(self.motorList)

    def __getitem__(self, key):
        return self.motorList[key]

    def __setitem__(self, key, value):
        self.motorList[key] = value

    def __contains__(self, item):
        return True if item in [m.state for m in self.motorList]

    def checkReadyStates(self):
        for motor in self.motorList:
            if motor.state != 1:
                return False
        return True