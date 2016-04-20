#!/usr/bin/python
# -*- coding: latin-1 -*-

WALL = -1
UNDEFINEDPATH= 0
ENDPOINT = -2
class Celda(object):
    """Una celda del mapa"""
    def __init__(self, x, y, goal=False, start=False):
        self.x=x
        self.y=y
        self.north = UNDEFINEDPATH
        self.west = UNDEFINEDPATH
        self.south= UNDEFINEDPATH
        self.east= UNDEFINEDPATH
        self.currentTotalCost = 9999999
        self.currentCost = 99999999
        self.euristicCost = 99999999

        self.previousCelda = UNDEFINEDPATH
        self.goal = goal
        self.start= start



    def __str__(self):
        s= "Celda en la posicion %i, %i, con costo %i, y euristica de %i y total de %i " % (self.x, self.y, self.currentCost, self.euristicCost, self.currentTotalCost)
        return(s)

        






