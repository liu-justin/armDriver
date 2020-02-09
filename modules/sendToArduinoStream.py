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

def waitForTilde():
	msg = ser.read().decode("unicode_escape")
	
	while not msg.endswith("~"):
		msg += ser.read().decode("unicode_escape")

	print(f"Out of waiting! msg is: {msg}")

def sendToArduinoDict(motorList):
	for m in motorList: 
		print(f"To: sending {m.arduinoStartByte} {len(motorList)} times")

		# used serial.peek in arduino so i can remove the for loop that was here
		ser.write((m.arduinoStartByte).to_bytes(1, byteorder="big")) # write the start Byte of the motor to tell Arduino which motor
		waitForArduino("start receiving bytes")	# when i put this in the for loop, first one caught motor 1, but second one was too late for motor 0 and also caught motor 1

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

def communicateWithArduino(motorList):
	