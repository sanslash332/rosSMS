#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
import math
from SMSBot.movement import MovementManager
from SMSBot.kinect import KinectManager
from SMSBot.sound import SoundManager

from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist


class Robot(object):
    """ Clase contenedora que representa al robot en sí mismo, y contiene todos los manejadores y partes que utilizaremos de él para manipularlo. Kinect, movimiento, sonido, etc"""

    def __init__(self, orientacion):
        rospy.init_node('TurtleBot', anonymous=True)        
        self.movement = MovementManager()
        self.kinect = KinectManager()
        self.sound = SoundManager()
	self.orientacionActual = orientacion

    def correctDistance(self, targetDist):
	dist = self.kinect.getDistance(320, 240)
	#rospy.loginfo("Initial distance = " + str(dist))	
	while(abs(dist-targetDist)>0.01):	
		velx = 1*(dist-targetDist)
		self.movement.setVelX(velx)
		dist = self.kinect.getDistance(320, 240)
	self.movement.stop()
	self.sound.say("distance corrected")
	#rospy.loginfo("Final distance = " + str(dist))

    def correctAlignment(self): 
	a = self.kinect.getAlignment()
	while(abs(a) > 0.004):
		vela = 100*a
		self.movement.setVelA(vela)
		a = self.kinect.getAlignment()
	self.movement.stop()
	self.sound.say("aligned") 
	#rospy.loginfo("Final alignment = " + str(a))

    def correctWallInFront(self):
	if(self.kinect.getDistance(320, 240)<1):		
		self.correctAlignment()
		self.correctDistance(0.5)

    def sayNextMovement(self, ori):
	if ori == 'n':
		self.sound.say("moving north")
	elif ori == 'e':
		self.sound.say("moving east")
	elif ori == 's':
		self.sound.say("moving south")
	else:
		self.sound.say("moving west")

    def moveMaze(self, ori):
	self.sayNextMovement(ori)		
	if self.orientacionActual == 'n':
		if ori == 'n':
			self.advanceOneCell()
		elif ori == 'e':
			self.turnRight()				
			self.advanceOneCell()
		elif ori == 's':
			self.turnLeft()
			self.turnLeft()			
			self.advanceOneCell()
		else:
			self.turnLeft()			
			self.advanceOneCell()
	elif self.orientacionActual == 'w':
		if ori == 'w':
			self.advanceOneCell()
		elif ori == 'n':
			self.turnRight()				
			self.advanceOneCell()
		elif ori == 'e':
			self.turnLeft()
			self.turnLeft()				
			self.advanceOneCell()
		else:
			self.turnLeft()		
			self.advanceOneCell()
	elif self.orientacionActual == 's':
		if ori == 's':
			self.advanceOneCell()
		elif ori == 'w':
			self.turnRight()			
			self.advanceOneCell()
		elif ori == 'n':
			self.turnLeft()
			self.turnLeft()			
			self.advanceOneCell()
		else:
			self.turnLeft()			
			self.advanceOneCell()
	else:
		if ori == 'e':
			self.advanceOneCell()
		elif ori == 's':
			self.turnRight()		
			self.advanceOneCell()
		elif ori == 'w':
			self.turnLeft()
			self.turnLeft()			
			self.advanceOneCell()
		else:
			self.turnLeft()		
			self.advanceOneCell()
	self.orientacionActual = ori
	
    def advanceOneCell(self):
	self.moveStraight(0.8, 0.3)

    def turnLeft(self, align=True):
	if align:
		self.correctWallInFront()
	self.moveRotate(math.pi/2,1.5)

    def turnRight(self, align=True):
	if align:
		self.correctWallInFront()	
	self.moveRotate(-math.pi/2,1.5)

    def moveStraight(self, distance, vel, brakeHelp=True, obstacleDetect=True, frontThreshold = 0.52, sideThreshold =0.52):
        self.movement.rate.sleep()
        posxInit = self.movement.position.x
        posyInit = self.movement.position.y
        dist=0
        
        while(dist< distance):           
            if obstacleDetect and self.kinect.obstacleInFront(frontThreshold):
		#self.correctWallInFront()
                break # agregar deteccion del lado del obstaculo y enderezar
	    
            x = self.movement.position.x - posxInit
            y = self.movement.position.y - posyInit
            dist = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
            #rospy.loginfo("distancia: " + str(dist))
            velx=vel
            if brakeHelp:
                velx = 2*(distance - dist)
                if velx > vel:
                    velx=vel
		elif velx < 0.05:
                    velx=0.01
            if dist <= vel - 0.05: #Hace que la partida sea mas suave
		velx = dist + 0.05 
	    
            # gira si tiene un muro muy cerca a los lados
            vela = 0;
	    if self.kinect.obstacleOnRight(sideThreshold):
	    	vela = 1.5*velx/vel
	    if self.kinect.obstacleOnLeft(sideThreshold):
		vela = -1.5*velx/vel

	    self.movement.setVelX(velx)
	    self.movement.setVelA(vela)
            self.movement.rate.sleep()

        self.movement.stop()
        self.movement.rate.sleep()


    def moveRotate(self, angle, vel, brakeHelp=False): 
        self.movement.rate.sleep()        
        data = Twist()
        angInit = self.movement.getRadianAngle()

        ang2 = 0
        vela = vel
        if(angle < 0):
            vela = -vel
        if(angle > 0):
            while(ang2 < angle*0.88):
                ang3 = self.movement.getRadianAngle()
                if ang3<0 and angInit>0:
                    ang3 = self.movement.getRadianAngle() + 2*math.pi

                ang2 = ang3 - angInit
                if brakeHelp:
                    vela = self.kpa * (angle - ang2)
                if vela > vel:
                    vela=vel

		        #if abs(ang2) < 0.35: #Hace que la partida sea mas suave
			    #vela = 4 * ang2 - 0.05

                data.angular.z = vela
                self.movement.setVel(data)
                self.movement.rate.sleep()

            self.movement.stop()
            self.movement.rate.sleep()
        else:
            while(ang2 > angle*0.88):
                ang3 = self.movement.getRadianAngle()
                if ang3>0 and angInit<0:
                    ang3 = self.movement.getRadianAngle() - 2*math.pi

                ang2 = ang3 - angInit

                if brakeHelp:
                    vela = self.kpa * (angle - ang2)
                if vela > vel:
                    vela=vel

                #if abs(ang2) < 0.35: #Hace que la partida sea mas suave
                #    vela = 4 * ang2 + 0.05

                data.angular.z = vela
                self.movement.setVel(data)
                self.movement.rate.sleep()
            self.movement.stop()
            self.movement.rate.sleep()

