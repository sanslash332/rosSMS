#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from sound_play.msg import SoundRequest


class SoundManager(object):
    """ Clase que controla y maneja la administración del sonido """

    def __init__(self):
        
        self._soundPub = rospy.Publisher('robotsound', SoundRequest)
        self.say("Sound started")
    def playBuiltSound(self, snd):
        s = SoundRequest()
        s.sound = snd
        s.command = s.PLAY_ONCE
        
        self._soundPub.publish(s)





    def playSound(self, snd):
        s = SoundRequest()
        s.sound = s.PLAY_FILE
        s.command = s.PLAY_ONCE
        s.arg = snd
        self._soundPub.publish(s)



    def say(self, msg):
        s = SoundRequest()
        s.sound = s.SAY
        s.command= s.PLAY_ONCE
        s.arg=msg
        self._soundPub.publish(s)







    