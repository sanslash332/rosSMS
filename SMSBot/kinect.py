#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
import math
from sensor_msgs.msg import Image

import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError


class KinectManager(object):
    """ clase que maneja todo lo referente a la cámara, el kinect e imágenes"""
    def __init__(self):
               #rospy.init_node('TurtleBot_Kinect', anonymous=True)
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
                #rospy.loginfo("imagen depth recibida " + str(self.current_cv_depth_image.shape))
                #cv2.imshow("image_depth",D )
                #cv2.waitKey(10)
            except CvBridgeError, e:
                print e

    def rgb_handler(self, data):
        try:
            self.current_cv_rgb_image = numpy.asarray(self.bridge.imgmsg_to_cv(data,"bgr8"))[:,:540]
            #rospy.loginfo("imagen rgb recibida " + str(self.current_cv_rgb_image.shape))
            
            #cv2.imshow("image_rgb",self.current_cv_rgb_image )
            #cv2.waitKey(10)
            
        except CvBridgeError, e:
            print e
    
    def obstacleInFront(self, threshold):
        D = self.current_cv_depth_image
        banda = D[:, 300:370]
        dists = banda.mean(0);
        if(numpy.any(dists<threshold)):
            rospy.loginfo("STOP!!")            
	    return 1
        return 0
    
    def obstacleOnRight(self, threshold):
	D = self.current_cv_depth_image
        banda = D[230:250, 440:540]
        dists = banda.mean(0);
        if(numpy.any(dists<threshold)):
            return 1
        return 0    

    def obstacleOnLeft(self, threshold):
	D = self.current_cv_depth_image
        banda = D[230:250, 130:230]
        dists = banda.mean(0);
        if(numpy.any(dists<threshold)):
            return 1
        return 0  
	
    '''
    def hayPared(self,distancia_pared):        
        D = self.current_cv_depth_image
        """Aca yo veria si es que en un sector mas o menos grande, por ejemplo R[100:400, 150:350], es del mismo color    """
        banda = D[250:420, :]
        dist = banda.mean(0);
        #rospy.loginfo(str(dist))
        rospy.loginfo(str(numpy.mean(dist)))
        if(numpy.mean(dist) < distancia_pared):
            return 1            
        return 0
    '''

    def getSideAlignment(self):
        D = self.current_cv_depth_image
        """Ve dos de los lados y entrega la diferencia"""
        banda = D[230:250, :];
        a1 = numpy.mean(banda[:,100:120])
        a2 = numpy.mean(banda[:,520:540])
        return a2-a1
    
    def getAlignment(self):
	D = self.current_cv_depth_image
        """Ve dos puntos de una pared y entrega la diferencia"""
        banda = D[230:250, :];
        a1 = numpy.mean(banda[:,250:300])
        a2 = numpy.mean(banda[:,370:420])
        #rospy.loginfo(str(numpy.mean(a2-a1)))
        return a2-a1
    
    def showDepthImage(self):
        cv2.imshow("image_depth",self.current_cv_depth_image)    
        cv2.waitKey(10)

    def getRgbImage(self):
        return self.current_cv_rgb_image
        
    def getDepthImage(self):
        return self.current_cv_depth_image

    def getDistance(self, x, y):
        D = self.current_cv_depth_image
        #rospy.loginfo(str(self.current_cv_rgb_image.shape))
        #cv2.imshow("Depth", D)
        #cv2.waitKey(10)
        try:
            return np.mean(D[y-5:y+5,x-5:x+5])
        except:
            return 0

    def detectarObjeto(self):
    
        img = self.current_cv_rgb_image
        img = np.uint8(img)
        
        
        # convert the image to HSV
        hsv_img = cv2.cvtColor(img,  cv2.COLOR_BGR2HSV)
        
        # apply thresholds
        #threshold_img1 = cv2.inRange(hsv_img, (165, 155, 110), (250, 200, 150))  # red
        #threshold_img1a = cv2.inRange(hsv_img, (0, 155, 110), (10, 200, 150))  # red again
        threshold_img1 = cv2.inRange(hsv_img, (160, 100, 100), (179, 255, 255))  # otro red
        
        # determine the moments of the two objects
        threshold_img1 = numpy.asarray(threshold_img1)
        M = cv2.moments(threshold_img1, 0)
        area1 = M['m00']

        # there can be noise in the video so ignore objects with small areas
        if (area1 > 20000):
            # x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
            x1 = int(M['m10']/M['m00'])
            y1 = int(M['m01']/M['m00'])

            # draw circle
            cv2.circle(img, (x1, y1), 2, (0, 255, 0), 20)
            return (x1, y1)
        #cv2.imshow("Object", threshold_img1)
        #cv2.imshow("Target", img)
        #cv2.waitKey(10)
        return (320, 240)
    


