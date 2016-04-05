#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy


class KinectManager(object):
    """ clase que maneja todo lo referente a la cámara, el kinect e imágenes"""
	def __init__(self):
       		rospy.init_node('/SMSBot/Kinect', anonymous=True)
		self.__depth_img = rospy.Subscriber('/camera/depth/image',Image ,self.depth_handler)
 		self.__rgb_img= rospy.Subscriber('/camera/rgb/image_color',Image,self.rgb_handler)
		self.bridge = CvBridge()
        	self.current_cv_depth_image = numpy.zeros((1,1,3))
        	self.current_cv_rgb_image = numpy.zeros((1,1,3))


	def depth_handler(self, data):
			try:
				D = numpy.asarray(self.bridge.imgmsg_to_cv(data,"32FC1"))[:,:540]
				D = numpy.ma.masked_array(D, numpy.isnan(D))
				self.current_cv_depth_image = D
				#cv2.imshow("image_depth",D )
				#cv2.waitKey(10)
			except CvBridgeError, e:
				print e

	def rgb_handler(self, data):
		try:
		    self.current_cv_rgb_image = numpy.asarray(self.bridge.imgmsg_to_cv(data,"bgr8"))
		    rospy.loginfo("imagen rgb recibida " + str(self.current_cv_rgb_image.shape))
		    
		    #cv2.imshow("image_rgb",self.current_cv_rgb_image )
		    #cv2.waitKey(10)
		    
		except CvBridgeError, e:
		    print e
	
	def obstacleInFront(self, threshold):
		D = self.current_cv_depth_image
		banda = D[230:250, :]
		dists = banda1.mean(0);
		if(numpy.any(dists<threshold)):
			return 1
			rospy.loginfo("STOP!!")
		return 0
	
	def isWall(self):
		R = self.current_cv_rgb_image
		D = self.current_cv_depth_image
		"""Aca yo veria si es que en un sector mas o menos grande, por ejemplo R[100:400, 150:350], es del mismo color	"""
		banda = D2[100:350, :]
		dist = banda1.mean(0);
		if(numpy.mean(dist) < 0.7):
			return 1			
		return 0
	
	def getAlignment(self):
		D = self.current_cv_depth_image
		"""Ve dos puntos de una pared y entrega la diferencia"""
		banda = D[100:350, :];
		a1 = numpy.mean(banda[:,220:270])
		a2 = numpy.mean(banda[:,370:420])
		return a2-a1
		
	def getRgbImage(self):
		return self.__rgb_img
		
	def getDepthImage(self):
		return self.__depth_img
