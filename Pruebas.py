import rospy
import numpy

def main():
	D = numpy.random.rand(1,2,3)
	print(D)
	print(D[:,:,0:2])

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
