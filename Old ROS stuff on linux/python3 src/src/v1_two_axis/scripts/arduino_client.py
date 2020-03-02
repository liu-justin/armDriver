#!/usr/bin/env python

import sys
import rospy
from v1_3axis.srv import *
import pointFinder as p
import stepFinder as s
import Motor
import MotorList
import serial

# for the comport, look in Arduino IDE when the arduino is connected
ser = serial.Serial("COM4", 57600)

def waitForArduino(passcode):
	msg = ser.read().decode("unicode_escape")
	
	while not msg.endswith(passcode):
		msg += ser.read().decode("unicode_escape")
		if (msg.endswith('~')):
			print(f"Periodic update: {msg}")
			msg = ""

	print(f"msg is: {msg}")

def initiateWithArduino(motorList):
	for m in motorList:
		for _ in range(2):

			m.tupleCounter += 1 # get off index 0, because the deltas are zero
			print(f"sending {m.arduinoStartByte} {m.stepTuple[m.tupleCounter][2]} {m.stepTuple[m.tupleCounter][3]}")
			ser.write((m.arduinoStartByte).to_bytes(1, byteorder="big")) # start byte
			ser.write((m.stepTuple[m.tupleCounter][2]).to_bytes(1, byteorder="big")) # delta time byte
			ser.write((m.stepTuple[m.tupleCounter][3]).to_bytes(1, byteorder="big")) # delta dir byte

	waitForArduino("}")

def communicateWithArduino():
	# msg received will be an index, need to navigate to the correct motor and send the correct values
	index = int.from_bytes(ser.read(), byteorder='big')
    time, direction = arduino_client(index)
	print(f"received index {index}")

    ser.write((startByte).to_bytes(1, byteorder="big")) # start byte
    ser.write((time).to_bytes(1, byteorder="big")) # delta time byte
    ser.write((direction).to_bytes(1, byteorder="big")) # delta dir byte


# since I only have one arduino now, I'll just use my previous code
# but to use two arduinos, I can use two arduino services for each of the motors
def arduino_client(startByte):
    rospy.wait_for_service('steps_to_arduino')
    try:
        fetching_next_steps = rospy.ServiceProxy('fetching_next_steps', NextStep)
        response = fetching_next_steps(startByte)
        return response.time, response.direction
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def arduino_client_init():
    waitForArduino("{")
    initiateWithArduino()
    communicateWithArduino()