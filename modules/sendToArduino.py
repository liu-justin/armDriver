import serial
import numpy as np
import time

# for the comport, look in Arduino IDE when the arduino is connected
ser = serial.Serial("COM8", 9600);

def waitForArduino(passcode):
	msg = ser.read().decode("unicode_escape")
	
	while not msg.endswith(passcode):
		msg += ser.read().decode("unicode_escape")
		if (msg.endswith('~')):
			print(f"Periodic update: {msg}")
			msg = ""

	print(f"---------------------------------------Out of waiting! msg is: {msg}")

def waitForTilde():
	msg = ser.read().decode("unicode_escape")
	
	while not msg.endswith("~"):
		msg += ser.read().decode("unicode_escape")

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

		# sending the startByte twice to catch the correct motor wherever the loop is
		for i in range(len(motorList)):
			ser.write((m.arduinoStartByte).to_bytes(1, byteorder="big")) # write the start Byte of the motor to tell Arduino which motor
			waitForArduino("Arduino received a start receiving byte")	

		previousTime = next(iter(m.stepDict.items()))[0]
		previousStep = next(iter(m.stepDict.items()))[1]

		# the very first step will send 0 for time and 0 for step, the Arduino will wait 0ms and step 0 steps
		# it is useless, but I can't find a way around it with a dict, and its benign so whatever

		print(f"To: sending time and dir data now")

		for time,step in m.stepDict.items():
			# if all this data is sent at once, Arduino can only fit 64 bytes into its que, the rest get dumped
			# ABOVE IS NOT TRUE - if you get rid of all Serial communication updates, then Arduino runs thru the que faster than Python can fill it up

			timeSent = int(round(time*1000 - previousTime)) # rounding the distance, not the times then the distance; also time needs to be converted into ms
			#print(f"To: time sent is - {timeSent}")
			previousTime = time*1000 						# update previousTime
			
			ser.write((timeSent).to_bytes(1, byteorder="big")) # send the time to Arduino
			print(f"To: sending time and dir data now")
			waitForArduino("Arduino received a time byte;") # waiting for Arduino to receive a time byte before sending a direction byte

			dirSent = int(np.sign(step)) + 121
			dirSent = int(np.sign(step - previousStep)) + 121 # find out if this step is >/</= previous, add to 121 for Arduino (is a flag)
			previousStep = step
			ser.write((dirSent).to_bytes(1, byteorder="big"))
			#print(f"To: direction sent is - {dirSent}")

		ser.write((102).to_bytes(1, byteorder="big")) #102 is the endMark
		print(f"To: sent 102, an endmark")
		waitForArduino("Arduino received an endMark;")

	while 1==1:
		waitForTilde()