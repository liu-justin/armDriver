import serial
import numpy as np

ser = serial.Serial("COM8", 9600);

def waitForArduino():
    msg = ""
    while msg.find("Arduino Ready") == -1:
        while ser.inWaiting() == 0:
            x = 'z'
        x = 'z'
        while ord(x) != endMarker:
            x = ser.read()
            msg = msg + x

def sendToArduino(timeR, stepR, timeC, stepC):
	# the sending code is time then step
	# timeR is sent in seconds, need to convert to milliseconds and round

	# byte for Arduino to start reading
	ser.write((101).to_bytes(1, byteorder-"big"))

	for i in range(1,len(timeR)):
		timeMS = round(timeR[i]*1000)
		ser.write((timeMS).to_bytes(1, byteorder="big"))
		stepDirection = np.sign(stepR[i+1] - stepR[i]) + 124 # plus 124 to get 123,124,125, bytes that i allocated for stepDirection
		ser.write((stepDirection).to_bytes(1, byteorder="big"))

	# byte to start end reading motorR and store it
	ser.write((103).to_bytes(1, byteorder-"big"))

	for i in range(len(timeC)-1):
		timeMS = round(timeC[i]*1000)
		ser.write((timeMS).to_bytes(1, byteorder="big"))
		stepDirection = np.sign(stepC[i+1] - stepC[i]) + 124 # plus 124 to get 123,124,125, bytes that i allocated for stepDirection
		ser.write((stepDirection).to_bytes(1, byteorder="big"))

	# byte to start end reading motorC and store it
	ser.write((104).to_bytes(1, byteorder-"big"))

	# byte to ending reading and start stepping
	ser.write((102).to_bytes(1, byteorder-"big"))

	# confirmation
	print(ArduinoSerial.readline())

