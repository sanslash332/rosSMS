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
	while True:
		tortuga.kinect.showDepthImage()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass

