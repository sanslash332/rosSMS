#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
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

    def __init__(self):
        rospy.init_node('TurtleBot', anonymous=True)        
        self.movement = MovementManager()
        self.kinect = KinectManager()
        self.sound = SoundManager()



    def moveStraight(self, distance, vel, brakeHelp=False, obstacleDetect=False, obsThreshold = 0.5):

        self.movement.rate.sleep()
        posxInit = self.movement.position.x
        posyInit = self.movement.position.y
        dist=0
        
        while(dist< distance):           
            if obstacleDetect and self.kinect.obstacleInFront(obsThreshold):
                break
            x = self.movement.position.x - posxInit
            y = self.movement.position.y - posyInit
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
            self.movement.setVel(data)
            self.movement.rate.sleep()

        data=Twist()
        self.movement.setVel(data)
        self.rate.sleep()


    def moveRotate(self, angle, vel, brakeHelp=False): 
        self.rate.sleep()        
        data = Twist()
        angInit = self.movement.getRadianAngle()

        ang2 = 0
        vela = vel
        if(angle < 0):
            vela = -vel
        if(angle > 0):
            while(ang2 < angle*0.8):
                ang3 = self.movement.getRadianAngle()
                if ang3<0 and angInit>0:
                    ang3 = self._angle + 2*math.pi

                ang2 = ang3 - angInit
                if brakeHelp:
                    vela = self.kpa * (angle - ang2)
                if vela > vel:
                    vela=vel

		        #if abs(ang2) < 0.35: #Hace que la partida sea mas suave
			    #vela = 4 * ang2 - 0.05

                data.angular.z = vela
                self.movement.setVel(data)
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
                self.movement.setVel(data)
                self.movement.rate.sleep()
            data = Twist()		
            self.movement.setVel(data)

