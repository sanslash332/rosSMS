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
from PID import PIDController
from kinect import KinectManager


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

    def moveStraight(self, distance, vel, brakeHelp=False, obstacleDetect=False, obsThreshold = 0.5):

	self.rate.sleep()
        posxInit = self._posX
        posyInit = self._posY
        dist=0
        
        kinect = KinectManager()
        
        while(dist< distance):           
            if obstacleDetect and kinect.obstacleInFront(obsThreshold):
            	break
            x = self._posX - posxInit
            y = self._posY - posyInit
            dist = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
	    rospy.loginfo("distancia: " + str(dist))
            velx=vel
            if brakeHelp:
                velx = self.kpx * (distance - dist)
                if velx > vel:
                    velx=vel
	    #if dist < 0.4: #Hace que la partida sea mas suave
		#velx = dist 


	    data = Twist()
            data.linear.x = velx
            self.setVel(data)
            self.rate.sleep()

        data=Twist()
        self.setVel(data)
	self.rate.sleep()


    def moveRotate(self, angle, vel, brakeHelp=False): 
        data = Twist()
        angInit = self._angle
        ang2 = 0
	vela = vel
	if(angle < 0):
	    vela = -vel
	if(angle > 0):
		while(ang2 < angle):
		    ang3 = self._angle
		    if ang3<0 and angInit>0:
		        ang3 = self._angle + 2*math.pi

		    ang2 = ang3 - angInit

		    if brakeHelp:
		        vela = self.kpa * (angle - ang2)
		        if vela > vel:
		            vela=vel

		    if abs(ang2) < 0.35: #Hace que la partida sea mas suave
			vela = 4 * ang2 - 0.05

		    data.angular.z = vela
		    self.setVel(data)
		    self.rate.sleep()
		data = Twist()		
		self.setVel(data)
	else:
		while(ang2 > angle):
		    ang3 = self._angle
		    if ang3>0 and angInit<0:
		        ang3 = self._angle - 2*math.pi

		    ang2 = ang3 - angInit

		    if brakeHelp:
		        vela = self.kpa * (angle - ang2)
		        if vela > vel:
		            vela=vel

		    if abs(ang2) < 0.35: #Hace que la partida sea mas suave
			vela = 4 * ang2 + 0.05

		    data.angular.z = vela
		    self.setVel(data)
		    self.rate.sleep()
		data = Twist()		
		self.setVel(data)

    def alinear(kinect):
	a = kinect.getAlignment()
	while(abs(a) > 0.03):
		a = kinect.getAlignment()
		data = Twist()
		vel = 100*self.al_dif
		if(vel > 2):
			vel = 2
		elif(vel < -2):
			vel = -2
		data.angular.z = vel
		self._nav_pub.publish(data)
	data = Twist()		
	self.nav_pub.publish(data)
    
    def getPosition(self):
        return(self._position)

    def getOrientation(self):
        return(self._orientation)

    def getRadianAngle(self):        
        return(self._angle)

