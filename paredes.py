#!/usr/bin/python
# -*- coding: latin-1 -*-
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
    	
	counter = 0	 	
	while counter < 4:
 		if tortuga.kinect.hayPared(0.7):
			rospy.loginfo(str(counter+1) + " hay pared")
			tortuga.sound.say("WALL")
			a = tortuga.kinect.getAlignment()
			#rospy.loginfo("align antes: "+str(a))
			while(abs(a) > 0.002):
				vela = 100*a
				if(vela > 1):
					vela = 1
				elif(vela < -1):
					vela = -1
				tortuga.movement.setVelA(vela)
				a = tortuga.kinect.getAlignment()
			#Decir que hay pared
			#rospy.loginfo("align despues: "+str(a))
			tortuga.movement.stop()
		else:
			tortuga.sound.say("NOTHING")
		time.sleep(1)
		tortuga.movement.moveRotate(math.pi/2, 2) 
		counter+=1
	tortuga.movement.stop()

 	

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
