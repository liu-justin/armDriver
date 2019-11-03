import modules.motorDriver as m
import modules.pointFinder as p
import modules.sendToArduino as s

import time

def main():
	#singlePoint(1,9)
	#multiplePoint()
	startTime = time.perf_counter()
	first = p.Point(2, 9)
	second = p.Point(9,-9)
	angles = p.linearTravel(first, second)
	afterLTTime = time.perf_counter()

	if angles == None:
	    print("angles is None, the linearTravel didn't go through the loop")
	    exit()
	else:
		#print(f"angleList: {angles}")
		#print(f"Length of angleList: {len(angles)}")
		data = m.getSteps(angles)

		s.waitForArduino()
		
		s.sendToArduino(data[0], data[1], data[2], data[3])
		afterGSTime = time.perf_counter()

	#print(f"{afterLTTime - startTime} : {afterGSTime - afterLTTime}")

main()
