import serial

ser = serial.Serial("COM4", 9600);

while 1==1:
	# msg = ser.read().decode("unicode_escape")
	msg = int.from_bytes(ser.read(), byteorder='big')
	print(f"This is msg: {msg}")
	print(msg+9)