#!/usr/bin/python
# -*- coding: latin-1 -*-
import rospy
import roslib
import numpy
import time

class PIDController(object):
    """ Clase para utilizar controladores del tipo PID"""

    def __init__(self, Kp, Ki, Kd):
        self.y = 0
        self.v = 0
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.er = (0, 0, 0)
        self.Taux = time.time()
        
    def calc_PID(e):
        end = time.time()
        dT = end - self.Taux
        
        self.er = (e, self.er[0], self.er[1])
        dv = Kp*(self.er[2]-self.er[1])+Ki*self.er[2]*dT+Kd*(self.er[2]-2*self.er[1]+self.er[0])/dT
        self.v = self.v + dv
        
        self.Taux = end
        
        return self.v
        
