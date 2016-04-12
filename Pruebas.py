import rospy
import roslib
import numpy
import math
import cv2
import time
from SMSBot.robot import Robot

def main():
	tortuga = Robot()
	while (tortuga.kinect.getDepthImage().shape == (1,1,3)):
		rospy.loginfo("cargando kinect")
		x1 = 100
		y1 = 240
		x2 = 520
	while True:
		img = tortuga.kinect.getDepthImage()
		cv2.circle(img, (x1, y1), 2, (0, 255, 0), 20)
		cv2.circle(img, (x2, y1), 2, (0, 255, 0), 20)
		cv2.imshow("image_depth", img)	
		cv2.waitKey(10)
		rospy.loginfo("side alignment = " + str(tortuga.kinect.getSideAlignment()))


if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass

