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
 	centerX = 320
 	centerY = 240
	x1 = 100
	y1 = 240
	x2 = 520
	dist = tortuga.kinect.getDistance(centerX, centerY)
	a = tortuga.kinect.getAlignment()
	while(abs(a) > 0.004 and dist < 1):
		vela = 100*a
		tortuga.movement.setVelA(vela)
		rospy.loginfo(a)
		a = tortuga.kinect.getAlignment()
		dist = tortuga.kinect.getDistance(centerX, centerY)
	tortuga.movement.stop()
	rospy.loginfo("aligned")
	dist = tortuga.kinect.getDistance(centerX, centerY)
	while(dist < 0.8):
		tortuga.moveRotate(math.pi/2, 2) 
		rospy.loginfo("rotate")
		dist = tortuga.kinect.getDistance(centerX, centerY)
		if not dist > 0:
			dist = 0.5
		rospy.loginfo("distance " + str(dist))
	rospy.loginfo("a!")	
	while(dist > 0.5):
		dist = tortuga.kinect.getDistance(centerX, centerY)
		a = tortuga.kinect.getSideAlignment()
		velx = 0.5*(dist-0.5)
		tortuga.movement.setVelX(velx)
		vela = -2 * a
		if(dist < 0.8):
			a = tortuga.kinect.getAlignment()
			vela = 2 * a
		tortuga.movement.setVelA(vela)
		img = tortuga.kinect.getDepthImage()		
		rospy.loginfo("side alignment = " + str(a))


	"""dist = tortuga.kinect.getDistance(centerX, centerY)
	while tortuga.kinect.hayPared(0.7):
		while(abs(a) > 0.002):
			vela = 100*a
			if(vela > 1):
				vela = 1
			elif(vela < -1):
				vela = -1
			tortuga.movement.setVelA(vela)
			a = tortuga.kinect.getAlignment()
		tortuga.sound.say("ALIGNED")		
		time.sleep(1)
		tortuga.movement.moveRotate(math.pi/2, 2) 
	else:
		tortuga.sound.say("GO")	
	tortuga.movement.stop()
	a = tortuga.kinect.getAlignment()"""

	'''tortuga.movement.stop()
 	centerX = 320
 	centerY = 240
	dist = tortuga.kinect.getDistance(centerX, centerY)
	while dist > 0.7:		
		if(obstacle)		
		tortuga.movement.setVelX(0.3)'''
	'''
	dif = tortuga.kinect.getAlignment() 
	dist = tortuga.kinect.getDistance(centerX, centerY)
	if(dist > 0 and abs(dif) > 0):
		velx = 0.5*(dist-0.8)
		if(dist < 0.8):
			t=0
		if(t<1):
			t+=0.1
			if(velx > 0.3*t):
				velx = 0.3*t
		tortuga.movement.setVelX(velx)
		vela = 0.02* (dif)
		tortuga.movement.setVelA(vela)
		r.sleep()

	        
	r = rospy.Rate(10)
	t = 0
	distMax = 0
	angMax = 0
	while (tortuga.kinect.getDepthImage().shape == (1,1,3)):
		rospy.loginfo("cargando kinect")
 	while True:	
 		centerX = 320
 		centerY = 240	
		r.sleep()
		angInit = tortuga.movement.getRadianAngle()
		ang = angInit+0.1
		while ang != angInit:
			tortuga.movement.setVelA(1.5)
			ang = tortuga.movement.getRadianAngle()
			dist = tortuga.kinect.getDistance(centerX, centerY)
			if dist > distMax:
				distMax = dist
				angMax = tortuga.movement.getRadianAngle()
		
		while ang != angMax:
			tortuga.movement.setVelA(1.5)
			ang = tortuga.movement.getRadianAngle()

		dif = tortuga.kinect.getAlignment()	 
		dist = tortuga.kinect.getDistance(centerX, centerY)
		if(dist > 0 and abs(dif) > 0):
			velx = 0.5*(dist-0.6)
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
	'''		
		

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
