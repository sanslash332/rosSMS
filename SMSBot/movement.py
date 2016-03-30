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
