class dictTest:
    def __init__(self):
        self.dict = {}
        self.angle = 1234
        self.dict["bangle"] = self.angle + 12
    
    @property
    def angle(self):
        return self.dict["angle"]

    @angle.setter
    def angle(self, newAngle):
        self.dict["angle"] = newAngle

a = dictTest()

def changeAttribute(param, val):
    a.dict[param] = val

print(a.angle)
changeAttribute("angle", 42)
print(a.angle)
