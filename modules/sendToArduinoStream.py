import serial
import numpy as np
import time

# for the comport, look in Arduino IDE when the arduino is connected
ser = serial.Serial("COM4", 57600);

def waitForArduino(passcode):
	msg = ser.read().decode("unicode_escape")
	
	while not msg.endswith(passcode):
		msg += ser.read().decode("unicode_escape")
		if (msg.endswith('~')):
			print(f"Periodic update: {msg}")
			msg = ""

	print(f"msg is: {msg}")

# dir is sent tail end, where the change in step happens at the end of the period
def initiateWithArduinoCalcInside(motorList):
	for m in motorList:
		for _ in range(2):
			m.tupleCounter += 1
			ser.write((m.arduinoStartByte).to_bytes(1, byteorder="big")) # start byte
			timeSent = int(round(1000*(m.stepTuple[m.tupleCounter][0] - m.stepTuple[m.tupleCounter-1][0])))
			ser.write((timeSent).to_bytes(1, byteorder="big")) # time byte
			dirSent = int(np.sign(m.stepTuple[m.tupleCounter][1] - m.stepTuple[m.tupleCounter-1][1])) + 121
			ser.write(().to_bytes(1, byteorder="big")) # dir byte

	waitForArduino("}")

# stepTuple is a list of tuples, of form (time, step, deltatime, deltastep), this function uses the delta
def initiateWithArduino(motorList):
	for m in motorList:
		for _ in range(2):

			m.tupleCounter += 1 # get off index 0, because the deltas are zero
			print(f"sending {m.arduinoStartByte} {m.stepTuple[m.tupleCounter][2]} {m.stepTuple[m.tupleCounter][3]}")
			ser.write((m.arduinoStartByte).to_bytes(1, byteorder="big")) # start byte
			ser.write((m.stepTuple[m.tupleCounter][2]).to_bytes(1, byteorder="big")) # delta time byte
			ser.write((m.stepTuple[m.tupleCounter][3]).to_bytes(1, byteorder="big")) # delta dir byte

	waitForArduino("}")

def communicateWithArduino(motorList):
	# msg received will be an index, need to navigate to the correct motor and send the correct values
	index = int.from_bytes(ser.read(), byteorder='big')
	#index = ser.read()
	#print(f"index type: {type(index)}")
	print(f"received index {index}")

	motorList[index].tupleCounter += 1
	if (motorList[index].tupleCounter < len(motorList[index].stepTuple)):
		ser.write((motorList[index].arduinoStartByte).to_bytes(1, byteorder="big")) # start byte
		ser.write((motorList[index].stepTuple[motorList[index].tupleCounter][2]).to_bytes(1, byteorder="big")) # delta time byte
		ser.write((motorList[index].stepTuple[motorList[index].tupleCounter][3]).to_bytes(1, byteorder="big")) # delta dir byte
	
# if (smath.calcDivisorForMultiples(deltaT)>1):
#     divisor = smath.calcDivisorForMultiples(deltaT)
#     print(f"deltaT is greater than 60: {deltaT}, divisor is: {divisor} the stepTuple: {self.stepTuple}")
#     for k in range(0, deltaT%divisor):
#         self.stepTuple.append((self.stepTuple[-1][0]+math.ceil(deltaT/divisor)/1000, self.stepTuple[-1][1], math.ceil(deltaT/divisor), 121))
#     print(f"after the first one {self.stepTuple}")
#     for k in range(deltaT%divisor, divisor-deltaT%divisor-1):
#         self.stepTuple.append((self.stepTuple[-1][0]+math.floor(deltaT/divisor)/1000, self.stepTuple[-1][1], math.floor(deltaT/divisor), 121))                            
#     print(f"after the second one {self.stepTuple}")

def communicateWithArduinoSplit(motorList):
	# msg received will be an index, need to navigate to the correct motor and send the correct values
	index = int.from_bytes(ser.read(), byteorder='big')
	#index = ser.read()
	#print(f"index type: {type(index)}")
	print(f"received index {index}")

	motorList[index].tupleCounter += 1
	if (motorList[index].tupleCounter < motorList[index].stepTuple.length):
		# divisors = smath.calcDivisorForMultiples(motorList[index].stepTuple[motorList[index].tupleCounter][2])
		# for i in range(1,divisors):
		# 	ser.write((motorList[index].arduinoStartByte).to_bytes(1, byteorder="big")) # start byte
		# 	ser.write(int(round(motorList[index].stepTuple[motorList[index].tupleCounter][2]*i/divisors)).to_bytes(1, byteorder="big")) # delta time byte
		# 	ser.write((121).to_bytes(1, byteorder="big")) # delta dir byte
		ser.write((motorList[index].arduinoStartByte).to_bytes(1, byteorder="big")) # start byte
		ser.write((motorList[index].stepTuple[motorList[index].tupleCounter][2]).to_bytes(1, byteorder="big")) # delta time byte
		ser.write((motorList[index].stepTuple[motorList[index].tupleCounter][3]).to_bytes(1, byteorder="big")) # delta dir byte