import serial #Serial imported for Serial communication
import time #Required to use delay functions
import struct
import ctypes

ArduinoSerial = serial.Serial("COM8", 9600)
#time.sleep(2)
print (ArduinoSerial.readline())

x = 46
chrX = chr(x)
print(chrX)
#print(type(chrX))
print(hex(32))


ArduinoSerial.write((126).to_bytes(1, byteorder='big'))
ArduinoSerial.write('e'.encode())
ArduinoSerial.write((100).to_bytes(1, byteorder='big'))
ArduinoSerial.write('f'.encode())
ArduinoSerial.write((52).to_bytes(1, byteorder='big'))
ArduinoSerial.write('g'.encode())
ArduinoSerial.write('h'.encode())

while 1==1:
    print(ArduinoSerial.readline())
