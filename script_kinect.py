#-*- coding: utf-8 -*-

import rospy
import roslib
import numpy

from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge, CvBridgeError

class Turtlebot_Kinect(object):
    def __init__(self):
        self.__depth_img = rospy.Subscriber('/camera/depth/image',Image ,self.__depth_handler)
        self.__rgb_img= rospy.Subscriber('/camera/rgb/image_color',Image,self.__rgb_handler)
        self.bridge = CvBridge()
        self.current_cv_depth_image = numpy.zeros((1,1,3))
        self.current_cv_rgb_image = numpy.zeros((1,1,3))

    def __depth_handler(self, data):
        try:
            self.current_cv_depth_image = numpy.asarray(self.bridge.imgmsg_to_cv(data,"32FC1"))
            rospy.loginfo("imagen depth recibida " + str(self.current_cv_depth_image.shape))
            
        except CvBridgeError, e:
            print e

    def __rgb_handler(self, data):
        try:
            self.current_cv_rgb_image = numpy.asarray(self.bridge.imgmsg_to_cv(data,"bgr8"))
            rospy.loginfo("imagen rgb recibida " + str(self.current_cv_rgb_image.shape))
            
            # concateno ambas imágenes sólo para visualización
            I = self.current_cv_rgb_image
            D = numpy.zeros((I.shape[0], I.shape[1],3), numpy.uint8)
            if self.current_cv_depth_image.shape[:2] == self.current_cv_rgb_image.shape[:2]:
                rospy.loginfo("imagen concatenada")
                D[:,:,0] = self.current_cv_depth_image*40 # sólo para visualización
                D[:,:,1] = D[:,:,0]
                D[:,:,2] = D[:,:,1]
            
            cv2.imshow("image_rgb",numpy.concatenate((I,D),axis=1))
            cv2.waitKey(10)
            
        except CvBridgeError, e:
            print e


if __name__ == '__main__':
    rospy.init_node("test_move_action_client")
    
    handler = Turtlebot_Kinect()
    
    rospy.spin()
    

