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
	for i in range(len(timeR)-1):
		timeMS = round((timeR[i+1] - timeR[i])*1000)
		ser.write((timeMS).to_bytes(1, byteorder="big"))
		stepDirection = np.sign(stepR[i+1] - stepR[i]) + 102 # plus 102 to get 101,102,103, bytes that i allocated for stepDirection
		ser.write((stepDirection).to_bytes(1, byteorder="big"))

	# send a byte signaling switch to C array now?

	for i in range(len(timeC)-1):
		timeMS = round((timeC[i+1] - timeC[i])*1000)
		ser.write((timeMS).to_bytes(1, byteorder="big"))
		stepDirection = np.sign(stepC[i+1] - stepC[i]) + 102 # plus 102 to get 101,102,103, bytes that i allocated for stepDirection
		ser.write((stepDirection).to_bytes(1, byteorder="big"))


