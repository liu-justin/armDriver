import modules.motorDriver as m
import modules.pointFinder as p


def main():
	#singlePoint(1,9)
	#multiplePoint()

	first = p.Point(2,2)
	second = p.Point(12,2)
	angles = p.linearTravel(first, second)
	if angles[0] == None:
	    print("angles is None, the linearTravel didn't go through the loop")
	    exit()
	else:
		#print(f"angleList: {angles}")
		print(f"Length of angleList: {len(angles)}")

	m.getSteps(angles)
    #p.drawAngleList(angles)
	#print("asdf")

main()