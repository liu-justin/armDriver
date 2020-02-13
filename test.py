# import serial

# ser = serial.Serial("COM4", 9600);

# while 1==1:
# 	# msg = ser.read().decode("unicode_escape")
# 	msg = int.from_bytes(ser.read(), byteorder='big')
# 	print(f"This is msg: {msg}")
# 	print(msg+9)
# a = input("What state do you want to go to: ")
# print(a)

def splitTime(x):
	divisor = x//50+1
	return(x/divisor)

print(splitTime(239))


