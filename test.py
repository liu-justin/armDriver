# import serial

# ser = serial.Serial("COM4", 9600);

# while 1==1:
# 	# msg = ser.read().decode("unicode_escape")
# 	msg = int.from_bytes(ser.read(), byteorder='big')
# 	print(f"This is msg: {msg}")
# 	print(msg+9)
# a = input("What state do you want to go to: ")
# print(a)

import math

def splitTime(x):
	divisor = x//60+1
	exact = x/divisor
	roundedFract = x%divisor
	#return(x, divisor, exact, roundedFract, math.ceil(exact)*(roundedFract)+math.floor(exact)*(divisor - roundedFract))
	return divisor

a = splitTime(469)
print(a)
sumA = 0
for i in range(1,a+1):
	b = int(round(469*i/a))
	sumA += b
	print (f"b: {b}")

	3.8328
	3.5149