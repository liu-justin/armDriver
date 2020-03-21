import modules.pointFinder as p
import modules.basicShapes as bs
import modules.motor as motor
import modules.MotorList as MotorList

def main():
	first = bs.Point(7,9)
	p.singlePoint(first)
	# bs.MAINARM.angle_VT_RR_RO = 0
	# bs.linkC.angle = 52
	# print(bs.linkC.outside)
	# p.torquePointPlot()
	# p.adjustmentsPlot("length_RR_RO")
main()