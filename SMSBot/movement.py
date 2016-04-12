#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
import math
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from SMSBot.PID import PIDController


class MovementManager(object):
    """ clase que controla y maneja el movimiento del robot"""

    def __init__(self):
        #rospy.init_node('TurtleBot_Movement', anonymous=True)
        self.vel=0.3
        self.vela=1.5
        self.rate = rospy.Rate(10)
        self.odomSub = rospy.Subscriber('/odom',Odometry,self.callback)
        self._navPub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist)
        self._odomData = Odometry()
        self._vel = Twist()
        self.position= None
        self._posX = 0
        self._posY = 0
        self._orientation = None
        self._angle=0
        self.kpx=0.1
        self.kpa=0.1

    def callback(self, data):
        self._odomData=data
        position=data.pose.pose.position
        self._posX = position.x
        self._posY = position.y
        self.position = position
        self._orientation=data.pose.pose.orientation
        self._angle= euler_from_quaternion([self._orientation.x, self._orientation.y, self._orientation.z, self._orientation.w])[2]

        
    def setVel(self, data):
        self._navPub.publish(data)
    def setVelA(self, vel):
	vela = vel
	if(vel > 2):
		vela = 2
	elif(vel < -2):
		vela = -2
	self._vel.angular.z = vela
        self._navPub.publish(self._vel)
    def setVelX(self, vel):
	velx = vel
	if(vel > 0.5):
		velx = 0.5
	elif(vel < -0.5):
		velx = -0.5
	self._vel.linear.x = velx
        self._navPub.publish(self._vel)
    def stop(self):
        data = Twist()
        self._navPub.publish(data)

    def getPosition(self):
        return(self._position)

    def getOrientation(self):
        return(self._orientation)

    def getRadianAngle(self):        
        return(self._angle)

