#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
from SMSBot.movement import MovementManager
from SMSBot.kinect import KinectManager
from SMSBot.sound import SoundManager

class Robot(object):
    """ Clase contenedora que representa al robot en sí mismo, y contiene todos los manejadores y partes que utilizaremos de él para manipularlo. Kinect, movimiento, sonido, etc"""

    def __init__(self):
        self.movement = MovementManager()
        self.kinect = KinectManager()
        self.sound = SoundManager()

