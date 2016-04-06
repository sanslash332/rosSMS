#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
from movement import MovementManager
from kinect import KinectManager
from sound import SoundManager

class Robot(object):
    """ Clase contenedora que representa al robot en sí mismo, y contiene todos los manejadores y partes que utilizaremos de él para manipularlo. Kinect, movimiento, sonido, etc"""

    def __init__(self):
        rospy.init_node('TurtleBot', anonymous=True)        
        self.movement = MovementManager()
        self.kinect = KinectManager()
        self.sound = SoundManager()

