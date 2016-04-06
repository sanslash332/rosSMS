#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
import math
import cv2
from robot import Robot
from PID import PIDController

def main():
 	tortuga = Robot()
        r = rospy.Rate(10)
 	#spinPID = PIDController(0.1,0.1,0.1)
	t = 0
 	while True:
		(targetX, targetY) = tortuga.kinect.detectarObjeto() 	
 		centerX = 320
		dif = centerX - targetX	 
		dist = tortuga.kinect.getDistance(targetX, targetY)
		if(dist > 0 and abs(dif) > 0):
			velx = 0.2*(dist-0.6)
			if(dist < 0.8):
				t=0
			if(t<1):
				t+=0.1
				if(velx > 0.3*t):
					velx = 0.3*t
			tortuga.movement.setVelX(velx)
			vela = 0.02* (dif)
			tortuga.movement.setVelA(vela)
			rospy.loginfo("dist = " + str(dist) + "dif = " + str(dif) + "vela = " + str(vela) + "velx = " + str(velx))
			r.sleep()

		"""if(abs(dif) < 30 and dist > 0 and abs(dif) > 0):
			velx = 0.2*(dist-0.6)
			if(t<1):
				velx = 0.3*t
			tortuga.movement.setVelX(velx)
			t+=0.1;
			r.sleep()
		else:
			vela = 0.02* (dif)
			tortuga.movement.setVelA(vela)
			t=0
		"""

 	

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	

        
			#avance	
