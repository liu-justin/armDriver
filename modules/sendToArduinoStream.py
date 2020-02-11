import serial
import numpy as np
import time

# for the comport, look in Arduino IDE when the arduino is connected
ser = serial.Serial("COM8", 57600);

def waitForArduino(passcode):
	msg = ser.read().decode("unicode_escape")
	
	while not msg.endswith(passcode):
		msg += ser.read().decode("unicode_escape")
		if (msg.endswith('~')):
			print(f"Periodic update: {msg}")
			msg = ""

	print(f"---------------------------------------Out of waiting! msg is: {msg}")

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

	waitForArduino("Ready to receive real data")

# stepTuple is a list of tuples, of form (time, step, deltatime, deltastep), this function uses the delta
def initiateWithArduino(motorList):
	for m in motorList:
		for _ in range(2):

			m.tupleCounter += 1 # get off index 0, because the deltas are zero
			print(f"sending {m.arduinoStartByte} {m.stepTuple[m.tupleCounter][2]} {m.stepTuple[m.tupleCounter][3]}")
			ser.write((m.arduinoStartByte).to_bytes(1, byteorder="big")) # start byte
			ser.write((m.stepTuple[m.tupleCounter][2]).to_bytes(1, byteorder="big")) # delta time byte
			ser.write((m.stepTuple[m.tupleCounter][3]).to_bytes(1, byteorder="big")) # delta dir byte

	waitForArduino("Ready to receive real data")

def communicateWithArduino(motorList):
	if ser.available():
		# msg received will be an index, need to navigate to the correct motor and send the correct values
		index = ser.read().decode("unicode_escape")
		print(f"received index {index}")

		motorList[index].tupleCounter += 1
		ser.write((motorList[index].arduinoStartByte).to_bytes(1, byteorder="big")) # start byte
		ser.write((motorList[index].stepTuple[motorList[index].tupleCounter][2]).to_bytes(1, byteorder="big")) # delta time byte
		ser.write((motorList[index].stepTuple[motorList[index].tupleCounter][3]).to_bytes(1, byteorder="big")) # delta dir byte

		# timeSent = int(round(motorList[index].stepTuple[motorList[index].tupleCounter][0] - motorList[index].stepTuple[motorList[index].tupleCounter-1][0]))
		# ser.write((timeSent).to_bytes(1, byteorder="big")) # time byte
		# dirSent = int(np.sign(motorList[index].stepTuple[motorList[index].tupleCounter][1] - motorList[index].stepTuple[motorList[index].tupleCounter-1][1])) + 121
		# ser.write(().to_bytes(1, byteorder="big")) # dir byte

