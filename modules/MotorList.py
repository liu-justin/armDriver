class MotorList:
    def __init__(self):
        # Arduino start reading bytes start at R0 motor, byte 103
        self._motorList = []

    def append(self, motor):
        self._motorList.append(motor)

    def __len__(self):
        return len(self._motorList)

    def __getitem__(self, key):
        return self._motorList[key]

    def __setitem__(self, key, value):
        self._motorList[key] = value

    def __contains__(self, item):

        return True if item in [m.state for m in self._motorList] else False

    def __str__(self):
        return str([m.state for m in self._motorList])

    def checkReadyStates(self):
        for motor in self._motorList:
            if motor.state != 1:
                return False
        return True