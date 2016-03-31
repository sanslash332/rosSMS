#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist


class MovementManager(object):
    """ clase que controla y maneja el movimiento del robot"""

    def __init__(self):
        rospy.init_node('/SMSBot/Movement', anonymous=True)
        self.vel=0.3
        self.vela=1.5
        self.rate = rospy.Rate(10)
        self.odomSub = rospy.Subscriber('/odom',Odometry,self.callback)
        self._navPub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist)
        self._odomData = Odometry()
        self._position = None
        self._orientation=None
        self._angle=0

    def callback(self, data):
        self._odomData=data
        self._position=data.pose.pose.position
        self._orientation=data.pose.pose.orientation
        self._angle= euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])[2]

        
    def setVel(self, data):
        self._navPub.publish(data)


    def moveRotate(self, angle, vel): 
        data = Twist()
        angInit = self._angle
        ang2 = 0
        data.angular.z = vel
        while(ang2 < angle):
            self.setVel(data)
            ang3 = self._angle
            if ang3<0 and angInit>0:
                ang3 = self._angle + 2*math.pi
            ang2 = ang3 - angInit
            self.rate.sleep()
        data = Twist()		
        self.setVel(data)


    def getPosition(self):
        return(self._position)

    def getOrientation(self):
        return(self._orientation)

    def getRadianAngle(self):
        
        return(self._angle)

