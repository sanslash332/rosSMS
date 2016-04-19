#-*- coding: utf-8 -*-

import rospy
import roslib
import numpy

import math
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import time

import cv2
from cv_bridge import CvBridge, CvBridgeError


# roslaunch openni_launch openni.launch
# rosrun image_view miage_view image:=/camera/rgb/image_color

class RobotMaze(object):
	def __init__(self, orientacion):
        	rospy.init_node('TurtleBot', anonymous=True)   
		self.stopSignal = 0
		self.vel = 0.3
		self.vela = 1.5	
		self.rate = rospy.Rate(10)
		self.ang = 0
		self.orientacionActual = orientacion
		self.odom_sub = rospy.Subscriber('/turtlebot/odom',Odometry,self.position_recv)
	    	self._navPub = rospy.Publisher('/turtlebot/cmd_vel', Twist)
		self.rate.sleep()

	def position_recv(self, data):
		pos = data.pose.pose.position
		quat = data.pose.pose.orientation
		self.posx = pos.x
		self.posy = pos.y
		self.ang = euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])[2]
	
	def move(self, ori):
		if self.orientacionActual == 'n':
			if ori == 'n':
				self.moveStraight(0.8, 0.3)
			elif ori == 'e':
				self.moveRotate(-math.pi/2,1.5) 				
				self.moveStraight(0.8, 0.3)
			elif ori == 's':
				self.moveRotate(math.pi/2,1.5)
				self.moveRotate(math.pi/2,1.5)				
				self.moveStraight(0.8, 0.3)
			else:
				self.moveRotate(math.pi/2,1.5)				
				self.moveStraight(0.8, 0.3)
		elif self.orientacionActual == 'w':
			if ori == 'w':
				self.moveStraight(0.8, 0.3)
			elif ori == 'n':
				self.moveRotate(-math.pi/2,1.5)				
				self.moveStraight(0.8, 0.3)
			elif ori == 'e':
				self.moveRotate(math.pi/2,1.5)
				self.moveRotate(math.pi/2,1.5)				
				self.moveStraight(0.8, 0.3)
			else:
				self.moveRotate(math.pi/2,1.5)			
				self.moveStraight(0.8, 0.3)
		elif self.orientacionActual == 's':
			if ori == 's':
				self.moveStraight(0.8, 0.3)
			elif ori == 'w':
				self.moveRotate(-math.pi/2,1.5)				
				self.moveStraight(0.8, 0.3)
			elif ori == 'n':
				self.moveRotate(math.pi/2,1.5)
				self.moveRotate(math.pi/2,1.5)				
				self.moveStraight(0.8, 0.3)
			else:
				self.moveRotate(math.pi/2,1.5)			
				self.moveStraight(0.8, 0.3)
		else:
			if ori == 'e':
				self.moveStraight(0.8, 0.3)
			elif ori == 's':
				self.moveRotate(-math.pi/2,1.5)				
				self.moveStraight(0.8, 0.3)
			elif ori == 'w':
				self.moveRotate(math.pi/2,1.5)
				self.moveRotate(math.pi/2,1.5)				
				self.moveStraight(0.8, 0.3)
			else:
				self.moveRotate(math.pi/2,1.5)			
				self.moveStraight(0.8, 0.3)

	def moveRotate(self, angle, vel, brakeHelp=False): 
		self.rate.sleep()        
		data = Twist()
		angInit = self.ang

		ang2 = 0
		vela = vel
		if(angle < 0):
		    vela = -vel
		if(angle > 0):
		    while(ang2 < angle*0.94):
		        ang3 = self.ang
		        if ang3<0 and angInit>0:
		            ang3 = self.ang + 2*math.pi

		        ang2 = ang3 - angInit

		        if vela > vel:
		            vela=vel

		        data.angular.z = vela
		        self.setVel(data)
		        self.rate.sleep()
		    data = Twist()		
		    self.setVel(data)
		else:
		    while(ang2 > angle*0.94):
		        ang3 = self.ang
		        if ang3>0 and angInit<0:
		            ang3 = self.ang - 2*math.pi

		        ang2 = ang3 - angInit

		        if vela > vel:
		            vela=vel

		        data.angular.z = vela
		        self.setVel(data)
		        self.rate.sleep()
		    data = Twist()		
		    self.setVel(data)

	def setVel(self, data):
		self._navPub.publish(data)
		
	
	def moveStraight(self, distance, vel, brakeHelp=False):

		self.rate.sleep()
		posxInit = self.posx
		posyInit = self.posy
		dist=0
	
		while(dist< distance):           
		    x = self.posx - posxInit
		    y = self.posy - posyInit
		    dist = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
		    rospy.loginfo("distancia: " + str(dist))
		    velx=vel
		    if brakeHelp:
			velx = self.kpx * (distance - dist)
			if velx > vel:
			    velx=vel

		    data = Twist()
		    data.linear.x = velx
		    self.setVel(data)
		    self.rate.sleep()

		data=Twist()
		self.setVel(data)
		self.rate.sleep()
		

"""
if __name__ == '__main__':
    rospy.init_node("Turtlebot_Maze")
    handler = Turtlebot_Maze()

    # script
    #for i in range(0,4):
   # 	handler.moveRotate(math.pi/2,1.5)
   # 	handler.rate.sleep()
    handler.moveStraight(0.8, 0.3)
    handler.moveStraight(0.8, 0.3)
    handler.moveRotate(math.pi/2,1.5) 
    handler.moveStraight(0.8, 0.3) 
    handler.moveRotate(math.pi/2,1.5) 
    handler.moveStraight(0.8, 0.3)
    handler.moveStraight(0.8, 0.3)
    handler.moveRotate(-math.pi/2,1.5)
    rospy.spin()
"""
    

