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

import cv2
from cv_bridge import CvBridge, CvBridgeError


# roslaunch openni_launch openni.launch
# rosrun image_view miage_view image:=/camera/rgb/image_color

class Turtlebot_Kinect(object):
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
		self.alineado = 0
	def __depth_handler(self, data):
		try:
			self.current_cv_depth_image = numpy.asarray(self.bridge.imgmsg_to_cv(data,"32FC1"))[:,:540]
			D = self.current_cv_depth_image
			cv2.imshow("image_depth", self.current_cv_depth_image)
			cv2.waitKey(10)
			#rospy.loginfo("imagen depth recibida " + str(self.current_cv_depth_image.shape))
			D2 = numpy.ma.masked_array(D, numpy.isnan(D))
			cv2.imshow("image_depth", D2)
			cv2.waitKey(10)
			banda1 = D2[230:250, :];
			dists1 = banda1.mean(0);
			#rospy.loginfo("dm1 " + str(dM1))
			#rospy.loginfo("dm2 " + str(dM2))
			#rospy.loginfo("dm3 " + str(dM3))
			#rospy.loginfo("dists1 size: " + str(dists1))
			
			self.stopSignal = 0
			#if(numpy.any(dists1<0.5)):
				#self.stopSignal = 1
				#rospy.loginfo("STOP!!")

		except CvBridgeError, e:
			print e
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
		while(self.alineado==0):
			d = self.dists1
			imin = numpy.argmin(d, axis=1)
			rospy.loginfo(str(imin))
			
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
		
		#data = Twist()		
		#self.nav_pub.publish(data)

if __name__ == '__main__':
    rospy.init_node("Turtlebot_Kinect")
    
    handler = Turtlebot_Kinect()
    
    rospy.spin()
    

