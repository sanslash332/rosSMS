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
        self.kpx=0.1

    def callback(self, data):
        self._odomData=data
        self._position=data.pose.pose.position
        self._orientation=data.pose.pose.orientation
        self._angle= euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])[2]

        
    def setVel(self, data):
        self._navPub.publish(data)

    def moveStraight(self, distance, vel, brakeHelp=False):
        data = Twist()
        posxInit =self._position.x
        posyInit = self._position.y
        dist=0
        
        while(dist< distance):
            x = self._position.x - posxInit
            y = self._position.y - posyInit
            dist = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
            velx=vel

            if brakeHelp:
                velx = self.kp * (distance - dist)
                if velx > vel:
                    velx=vel

	    if dist < 0.4: #Hace que la partida sea mas suave
		velx = dist 



            data.linear.x = velx
            self.setVel(data)
            self.rate.sleep()

        data=Twist()
        self.setVel(data)


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
		        vela = self.kp * (angle - ang2)
		        if vela > vel:
		            vela=vel

		    if abs(ang2) < 0.35: #Hace que la partida sea mas suave
			vela = 4 * ang2

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
		        vela = self.kp * (angle - ang2)
		        if vela > vel:
		            vela=vel

		    if abs(ang2) < 0.35: #Hace que la partida sea mas suave
			vela = 4 * ang2

		    data.angular.z = vela
		    self.setVel(data)
		    self.rate.sleep()
		data = Twist()		
		self.setVel(data)

    def alinear(kinect)
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
			self.nav_pub.publish(data)
		data = Twist()		
		self.nav_pub.publish(data)
    def getPosition(self):
        return(self._position)

    def getOrientation(self):
        return(self._orientation)

    def getRadianAngle(self):        
        return(self._angle)

