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
    counter = 0
 	while counter < 4:
 		if tortuga.kinect.hayPared():
			a = tortuga.kinect.getAlignment()
			while(abs(a) > 0.03):
				vela = 100*self.al_dif
				if(vela > 2):
					vela = 2
				elif(vela < -2):
					vela = -2
				tortuga.movement.setVelA(vela)
				a = tortuga.kinect.getAlignment()
			#Decir que hay pared
		time.sleep(1)
		tortuga.movement.moveRotate(math.pi/2, vela, brakeHelp=True): 
		counter++
	tortuga.movement.stop()
 	

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass