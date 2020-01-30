import serial
import numpy as np
import time

# for the comport, look in Arduino IDE when the arduino is connected
ser = serial.Serial("COM8", 9600);

def waitForArduino(passcode = '~'):
	msg = ser.read().decode("unicode_escape")
	
	while not msg.endswith(passcode):
		msg += ser.read().decode("unicode_escape")
		if (msg.endswith('~')):
			print(msg)

	print(f"Out of waiting! msg is: {msg}")

def sendToArduino(timeR, stepR, timeC, stepC):
	# the sending code is time then step
	# timeR is sent in seconds, need to convert to milliseconds and round

	# byte for Arduino to start reading
	#ser.write((101).to_bytes(1, byteorder="big"))

	# byte to start reading motorR and store it
	ser.write((105).to_bytes(1, byteorder="big"))
	print("sent 103 to start R array")

	for i in range(0,len(timeR)-1):
		timeMS = int(round(timeR[i+1]*1000)-round(timeR[i]*1000))
		print(f"timeMS: {timeMS}")
		ser.write((timeMS).to_bytes(1, byteorder="big"))
		stepDirection = int(np.sign(stepR[i+1]) - stepR[i]) + 121 # plus 124 to get 123,124,125, bytes that i allocated for stepDirection
		ser.write((stepDirection).to_bytes(1, byteorder="big"))
		#time.sleep(0.1)
		#print(f"this is what the Arduino sent back: {ser.read()}")
		waitForArduino()

	# byte to start reading motorC and store it
	ser.write((106).to_bytes(1, byteorder="big"))

	for i in range(len(timeC)-1):
		timeMS = int(round(timeC[i+1]*1000)-round(timeC[i]*1000))
		ser.write((timeMS).to_bytes(1, byteorder="big"))
		stepDirection = int(np.sign(stepC[i+1] - stepC[i])) + 121 # plus 124 to get 123,124,125, bytes that i allocated for stepDirection
		ser.write((stepDirection).to_bytes(1, byteorder="big"))
		#time.sleep(0.1)
		waitForArduino()

	# byte to ending reading and start stepping
	ser.write((102).to_bytes(1, byteorder="big"))

	# confirmation
	while 1==1:
		print(ser.readline())
		time.sleep(0.001)

def sendToArduinoDict(motorList):
	for m in motorList: 
		print(f"To: sending {m.arduinoStartByte} {len(motorList)} times")
		for i in range(len(motorList)):
			ser.write((m.arduinoStartByte).to_bytes(1, byteorder="big")) # write the start Byte of the motor to tell Arduino which motor
		waitForArduino("Arduino received a start receiving byte and it has a match;")
		previousTime = next(iter(m.stepDict.items()))[0]
		previousStep = next(iter(m.stepDict.items()))[1]

		# the very first step will send 0 for time and 0 for step, the Arduino will wait 0ms and step 0 steps
		# it is useless, but I can't find a way around it with a dict, and its benign so whatever

		for time,step in m.stepDict.items():
			timeSent = round(time) - previousTime
			ser.write((timeSent).to_bytes(1, byteorder="big"))
			stepSent = int(np.sign(step)) + 121
			ser.write((stepSent).to_bytes(1, byteorder="big"))

			waitForArduino()

	ser.write((102).to_bytes(1, byteorder="big"))

	# confirmation
	while 1==1:
		print(ser.readline())
		time.sleep(0.001)