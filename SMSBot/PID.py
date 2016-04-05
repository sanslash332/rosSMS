#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy

class PIDController(object):
    """ Clase para utilizar controladores del tipo PID"""

    def __init__(self, Kp, Ki, Kd):
        self.y = 0
        self.u = 0
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.er = (0, 0, 0)
        
    def calc_PID(e, dt):
        self.er = (e, self.er[0], self.er[1])
        du = Kp*(self.er[2]-self.er[1])+Ki*self.er[2]*dT+Kd*(self.er[2]-2*self.er[1]+self.er[0])/dt
        self.u = self.u + du
        
        return self.u
        
