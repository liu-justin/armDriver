import modules.motorDriver as m
import modules.pointFinder as p

import time

def main():
	#singlePoint(1,9)
	#multiplePoint()
	startTime = time.perf_counter()
	first = p.Point(9, 9)
	second = p.Point(11,-6)
	angles = p.linearTravel(first, second)
	afterLTTime = time.perf_counter()
	if angles[0] == None:
	    print("angles is None, the linearTravel didn't go through the loop")
	    exit()
	else:
		#print(f"angleList: {angles}")
		#print(f"Length of angleList: {len(angles)}")
		m.getSteps(angles)
		afterGSTime = time.perf_counter()

	#print(f"{afterLTTime - startTime} : {afterGSTime - afterLTTime}")

	

main()