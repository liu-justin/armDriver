import serial
import numpy as np
import time

ser = serial.Serial("COM4", 9600);

def waitForArduino():
    x = ser.read()
    print(f"Arduino's response (b'~' is good: {x}")
    while x != b'~':
    	x = ser.read()
    	print("waiting for Arduino, still reading!")

    print("Out of waiting!")

def sendToArduino(timeR, stepR, timeC, stepC):
	# the sending code is time then step
	# timeR is sent in seconds, need to convert to milliseconds and round

	# byte for Arduino to start reading
	#ser.write((101).to_bytes(1, byteorder="big"))

	# byte to start reading motorR and store it
	ser.write((103).to_bytes(1, byteorder="big"))

	for i in range(0,len(timeR)-1):
		timeMS = int(round(timeR[i+1]*1000)-round(timeR[i]*1000))
		print(timeMS)
		ser.write((timeMS).to_bytes(1, byteorder="big"))
		stepDirection = int(np.sign(stepR[i+1]) - stepR[i]) + 121 # plus 124 to get 123,124,125, bytes that i allocated for stepDirection
		ser.write((stepDirection).to_bytes(1, byteorder="big"))
		#time.sleep(0.1)
		print(f"this is what the Arduino sent back: {ser.read()}")
		#waitForArduino()

	# byte to start reading motorC and store it
	ser.write((104).to_bytes(1, byteorder="big"))

	for i in range(len(timeC)-1):
		timeMS = int(round(timeC[i+1]*1000)-round(timeC[i]*1000))
		ser.write((timeMS).to_bytes(1, byteorder="big"))
		stepDirection = int(np.sign(stepC[i+1] - stepC[i])) + 121 # plus 124 to get 123,124,125, bytes that i allocated for stepDirection
		ser.write((stepDirection).to_bytes(1, byteorder="big"))
		#time.sleep(0.1)
		#waitForArduino()

	# byte to ending reading and start stepping
	ser.write((102).to_bytes(1, byteorder="big"))

	# confirmation
	while 1==1:
		print(ser.readline())
		time.sleep(0.001)


