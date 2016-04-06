#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
import math
import cv2
import time
from robot import Robot
from PID import PIDController

def main():
 	tortuga = Robot()
        r = rospy.Rate(10)
 	#spinPID = PIDController(0.1,0.1,0.1)
	t = 0
 	while True:	
 		centerX = 320
 		centerY = 240
		dist = tortuga.kinect.getDistance(centerX, centerY)
		dif = tortuga.kinect.getSideAlignment()
		if(dist > 0 and abs(dif) > 0):
			velx = 0.2*(dist-0.6)
			if(dist < 0.8):
				t=0
			if(t<1):
				t+=0.1
				if(velx > 0.3*t):
					velx = 0.3*t
			tortuga.movement.setVelX(velx)
			vela = 0.03* (dif)
			tortuga.movement.setVelA(vela)

			if(velx < 0.001 and vela < 0.001)
				tortuga.movement.stop()
				break;
			rospy.loginfo("dist = " + str(dist) + "dif = " + str(dif) + "vela = " + str(vela) + "velx = " + str(velx))
			r.sleep()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass