import rospy
import roslib
import numpy
import math
import cv2
import time
from SMSBot.robot import Robot

def main():
	tortuga = Robot('n')
	r = rospy.Rate(10)
	while (tortuga.kinect.getDepthImage().shape == (1,1,3)):
		rospy.loginfo("cargando kinect")
		#pythonvalecallampa = 0
	while True:
		print tortuga.kinect.detectarLlave2(show = True)
		#tortuga.turnRight()
		#tortuga.turnRight()
		#tortuga.turnRight()
		#tortuga.turnRight()
		#tortuga.turnLeft()
		#tortuga.turnLeft()
		#tortuga.turnLeft()
		#tortuga.turnLeft()		
		r.sleep()
		


if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass

