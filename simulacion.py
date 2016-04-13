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

class Turtlebot_Maze(object):
	def __init__(self):
		self.__depth_img = rospy.Subscriber('/camera/depth/image',Image ,self.__depth_handler)
		self.bridge = CvBridge()
		self.current_cv_depth_image = numpy.zeros((1,1,3))
		self.stopSignal = 0
		self.vel = 0.3
		self.vela = 1.5	
		self.rate = rospy.Rate(10)
		self.odom_sub = rospy.Subscriber('/odom',Odometry,self.position_recv)
	    	self.nav_pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist)
		self.al_dif = 0
		self.alineado = 0
		self.ang = 0
		self.alinear()

	def position_recv(self, data):
		pos = data.pose.pose.position
		quat = data.pose.pose.orientation
		self.posx = pos.x
		self.posy = pos.y
		self.ang = euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])[2]
	def move_rotate(self, angle, vel): 
		data = Twist()
		ang_init = self.ang
		ang2 = 0
		data.angular.z = vel
		while(ang2 < angle):
			self.nav_pub.publish(data)
			ang3 = self.ang
			if ang3<0 and ang_init>0:
				ang3 = self.ang + 2*math.pi
			ang2 = ang3 - ang_init
			self.rate.sleep()
		data = Twist()		
		self.nav_pub.publish(data)
	def alinear(self):
		while(abs(self.al_dif) > 0.03):
			data = Twist()
			vel = 100*self.al_dif
			if(vel > 2):
				vel = 2
			elif(vel < -2):
				vel = -2
			data.angular.z = vel
			self.nav_pub.publish(data)
		data = Twist()		
		self.nav_pub.publish(data)
		time.sleep(1)		
	def move(self):
		while(1):
			if(self.stopSignal==1):
				data2 = Twist()
				self.nav_pub.publish(data2)
				rospy.loginfo("Spin")	
				self.move_rotate(math.pi/4, self.vela)	
			else:
				data1 = Twist()
				data1.linear.x = self.vel
				self.nav_pub.publish(data1) 	
			self.rate.sleep()
		

if __name__ == '__main__':
    rospy.init_node("Turtlebot_Maze")
    
    handler = Turtlebot_Kinect()
    
    rospy.spin()
    

